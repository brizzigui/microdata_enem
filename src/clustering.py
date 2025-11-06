from utils.read import read_socioeconomic_data_school_type

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
def cluster(data: list[list], types: list[int]) -> None:
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)

    n_clusters = 2
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(data_scaled)
    labels = kmeans.labels_

    counter = {}
    for i, label in enumerate(labels):
        if label not in counter:
            counter[label] = [0, 0]
        if types[i] == 4:
            counter[label][1] += 1
        else:
            counter[label][0] += 1

    for cluster_id in range(n_clusters):
        pub, priv = counter[cluster_id]
        total = pub + priv
        print(f"Socioeconomic cluster #{cluster_id}:")
        print(f"\t{100 * pub / total:.2f}% públicas,")
        print(f"\t{100 * priv / total:.2f}% privadas\n")

    pca = PCA(n_components=2)
    data_2d = pca.fit_transform(data_scaled)
    centers_2d = pca.transform(kmeans.cluster_centers_)

    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(data_2d[:, 0], data_2d[:, 1], c=labels, cmap='viridis', s=10)
    plt.scatter(
        centers_2d[:, 0], centers_2d[:, 1],
        c='red', s=200, marker='X', label='Centroids'
    )

    for i, (x, y) in enumerate(centers_2d):
        plt.text(x, y, f"C{i}", color='black', fontsize=12,
                 ha='center', va='center', fontweight='bold',
                 bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

    plt.title("Clustering K-Means (Dimensionalidade reduzida com PCA)")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.legend()
    plt.tight_layout()
    plt.savefig("./output/clustering/socioeconomic_schooltype.png", dpi=600)
    plt.close()



def evaluate():
    pass

def main() -> None:
    socioeconomic_data = read_socioeconomic_data_school_type()
    cleared_data = [v for v in socioeconomic_data if all(i != None for i in v)]
    del socioeconomic_data

    types = [v[0] for v in cleared_data]
    components = [v[1:] for v in cleared_data]
    cluster(components, types)

if __name__ == "__main__":
    main()