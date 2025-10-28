import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# we'll use kmeans to cluster questions
def fit(data):
    k = 100
    kmeans = KMeans(
        n_clusters=k,
        init="k-means++",
        n_init="auto",
        max_iter=300,
        random_state=42,
        verbose=1
    )

    # Fit model
    kmeans.fit(data)

    # Get results
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_

    print("Inertia:", kmeans.inertia_)
    print("Cluster centers shape:", centroids.shape)

# then compare with a manual classification
# evaluating how well a clustering based solution can classify questions
def evaluate():
    pass

def main() -> None:
    pass

if __name__ == "__main__":
    main()