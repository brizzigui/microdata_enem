import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

from utils.read import read_uf_grades_socioeconomic

std_upper = 650
std_lower = 450

def plot_avg(data: list[list]) -> None:
    state_sums = {}
    state_count = {}
    for v in data:
        # v[1] is the uf code
        if v[1] not in state_sums:
            state_sums[v[1]] = 0

        if v[1] not in state_count:
            state_count[v[1]] = 0

        state_sums[v[1]] += sum(v[2:])/5
        state_count[v[1]] += 1


    state_avgs = {}
    for k in state_sums.keys():
        state_avgs[k] = state_sums[k]/state_count[k]

    # loads shapefile
    # downloaded from ibge
    states = gpd.read_file("./src/geo/BR_UF_2024.shp")

    # adds values to map
    for i, row in states.iterrows():
        code = row['SIGLA_UF']
        states.at[i, 'value'] = state_avgs[code]

    # plots map
    fig, ax = plt.subplots(figsize=(8, 8))
    states.plot(column='value', ax=ax, legend=True, cmap="viridis", edgecolor='black',
                vmin=std_lower, vmax=std_upper)
    plt.title("Nota média do ENEM por UF")
    plt.axis('off')
    plt.savefig("./output/maps/avg_by_state.png", dpi=600, format="png")
    plt.close()

    with open("./output/maps/avg_rank.txt", 'w') as file:
        for k, v in sorted([*state_avgs.items()], key=lambda x: x[1], reverse=True):
            file.write(f"{k}, {v}\n")

def plot_rel_diff(data: list[list]) -> None:
    state_sums = {}
    state_count = {}
    for v in data:
        # v[1] is the uf code
        if v[1] not in state_sums:
            state_sums[v[1]] = [0, 0]

        if v[1] not in state_count:
            state_count[v[1]] = [0, 0]

        if int(v[0]) == 4:
            state_sums[v[1]][1] += sum(v[2:])/5
            state_count[v[1]][1] += 1

        else:
            state_sums[v[1]][0] += sum(v[2:])/5
            state_count[v[1]][0] += 1

    state_diff = {}
    state_public = {}
    state_private = {}
    for k in state_sums.keys():
        state_diff[k] = ((state_sums[k][1]/state_count[k][1])/(state_sums[k][0]/state_count[k][0]) - 1)*100
        state_public[k] = state_sums[k][0]/state_count[k][0]
        state_private[k] = state_sums[k][1]/state_count[k][1]

    # loads shapefile
    # downloaded from ibge
    states = gpd.read_file("./src/geo/BR_UF_2024.shp")

    # adds values to map
    for i, row in states.iterrows():
        code = row['SIGLA_UF']
        states.at[i, 'value'] = state_diff[code]

    # plots map
    fig, ax = plt.subplots(figsize=(8, 8))
    states.plot(column='value', ax=ax, legend=True, cmap="viridis", edgecolor='black')
    plt.title("Desigualdade relativa entre médias\ndas escolas públicas e privadas por UF")
    plt.axis('off')
    plt.savefig("./output/maps/diff_by_state.png", dpi=600, format="png")
    plt.close()

    # adds values to map
    for i, row in states.iterrows():
        code = row['SIGLA_UF']
        states.at[i, 'value'] = state_public[code]

    # plots map
    fig, ax = plt.subplots(figsize=(8, 8))
    states.plot(column='value', ax=ax, legend=True, cmap="viridis", edgecolor='black',
                vmin=std_lower, vmax=std_upper)
    plt.title("Nota média do ENEM por UF\ndentre escolas públicas")
    plt.axis('off')
    plt.savefig("./output/maps/public_by_state.png", dpi=600, format="png")
    plt.close()

    # adds values to map
    for i, row in states.iterrows():
        code = row['SIGLA_UF']
        states.at[i, 'value'] = state_private[code]

    # plots map
    fig, ax = plt.subplots(figsize=(8, 8))
    states.plot(column='value', ax=ax, legend=True, cmap="viridis", edgecolor='black',
                vmin=std_lower, vmax=std_upper)
    plt.title("Nota média do ENEM por UF\ndentre escolas privadas")
    plt.axis('off')
    plt.savefig("./output/maps/private_by_state.png", dpi=600, format="png")
    plt.close()

    with open("./output/maps/diff_by_state_rank.txt", 'w') as file:
        for k, v in sorted([*state_diff.items()], key=lambda x: x[1], reverse=True):
            file.write(f"{k}, {v}, {state_public[k]}, {state_private[k]}\n")


def main() -> None:
    data = read_uf_grades_socioeconomic()
    plot_avg(data)
    plot_rel_diff(data)

if __name__ == "__main__":
    main()
