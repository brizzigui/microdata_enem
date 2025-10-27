from utils.read import read_all_grades
import matplotlib.pyplot as plt
import numpy as np

def regression(points: list):
    labels = ["Ciências da Natureza", "Ciências Humanas", "Linguagens", "Matemática", "Redação"]

    for i in range(5):
        for j in range(i+1, 5):
            xy = sum([v[i]*v[j] for v in points])
            x = sum([v[i] for v in points])
            x2 = sum([v[i]**2 for v in points])
            y = sum([v[j] for v in points])
            y2 = sum([v[j]**2 for v in points])
            n = len(points)

            r = (n*xy - x*y)/((n*x2-x**2)*(n*y2 - y**2))**(1/2)
            print(f"{labels[i]} e {labels[j]}: r = {r}, r^2 = {r**2}")

            heatmap, xedges, yedges = np.histogram2d(
                [v[i] for v in points],
                [v[j] for v in points],
                bins=50,
                range=[[0, 1000], [0, 1000]]
            )
            extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

            plt.clf()
            plt.imshow(heatmap.T, extent=extent, origin='lower')
            plt.xlim(0, 1000)
            plt.ylim(0, 1000)
            plt.xlabel(labels[i])
            plt.ylabel(labels[j])
            plt.show()

def main() -> None:
    data = read_all_grades()
    regression(data)
    

if __name__ == "__main__":
    main()