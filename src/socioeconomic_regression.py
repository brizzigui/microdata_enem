from utils.read import read_socioeconomic_data
import matplotlib.pyplot as plt
import numpy as np

def regression(data: list):
    labels = [
        "Escolaridade do pai",
        "Escolaridade da mãe",
        "Grupo da ocupação do pai",
        "Grupo da ocupação da mãe",
        "Pessoas que moram na residência",
        "Renda familiar mensal",
        "Frequência de empregado doméstico",
        "Quantidade de banheiros na residência",
        "Quantidade de quartos na residência",
        "Quantidade de carros na residência",
        "Quantidade de motos na residência",
        "Quantidade de geladeiras na residência",
        "Quantidade de freezers na residência",
        "Quantidade de máquinas de lavar roupa na residência",
        "Quantidade de máquinas de secar roupa na residência",
        "Quantidade de micro-ondas na residência",
        "Quantidade de máquinas de lavar louça na residência",
        "Tem aspirador de pó na residência",
        "Quantidade de televisores na residência",
        "Quantidade de aparelhos de DVD na residência",
        "TV por assinatura na residência",
        "Quantidade de celulares na residência",
        "Telefone fixo na residência",
        "Quantidade de computadores na residência",
        "Tem acesso à internet na residência"
    ]

    print("Generating socioeconomic analysis plots")

    for q_index in range(1, 26):
        question_label = labels[q_index - 1]
        responses_dict = {}

        for row in data:
            avg_grade = row[0]
            response = row[q_index]

            if response is None or response == "":
                continue

            if response not in responses_dict:
                responses_dict[response] = []

            responses_dict[response].append(avg_grade)

        if len(responses_dict) == 0:
            print(f"No data for question Q{str(q_index).zfill(3)}")
            continue

        try:
            sorted_responses = sorted(responses_dict.keys(), key=lambda x: float(x))
        except (ValueError, TypeError):
            sorted_responses = sorted(responses_dict.keys())

        x_values = []
        y_values = []

        for resp in sorted_responses:
            try:
                x_val = float(resp)
                y_mean = np.mean(responses_dict[resp])
                x_values.append(x_val)
                y_values.append(y_mean)
            except (ValueError, TypeError):
                continue

        if len(x_values) > 1:
            n = len(x_values)
            xy = sum([x_values[i] * y_values[i] for i in range(n)])
            x = sum(x_values)
            x2 = sum([x**2 for x in x_values])
            y = sum(y_values)
            y2 = sum([y**2 for y in y_values])

            r = (n*xy - x*y)/((n*x2-x**2)*(n*y2 - y**2))**(1/2)

            a = (n*xy - x*y) / (n*x2 - x**2)
            b = (y - a*x) / n
            f = lambda x: a*x + b

        box_data = [responses_dict[resp] for resp in sorted_responses]

        plt.clf()
        fig, ax = plt.subplots(figsize=(10, 8))

        bp = ax.boxplot(box_data, tick_labels=sorted_responses, patch_artist=True, showfliers=False)

        for patch in bp['boxes']:
            patch.set_facecolor('lightblue')
            patch.set_alpha(0.7)

        for i, resp in enumerate(sorted_responses):
            values = responses_dict[resp]
            min_val = np.min(values)
            max_val = np.max(values)

            ax.plot([i + 1, i + 1], [min_val, max_val], 'k_', markersize=8, markeredgewidth=1.5)

        if a is not None and b is not None:
            try:
                x_numeric = [float(resp) for resp in sorted_responses]
                x_positions = list(range(1, len(sorted_responses) + 1))
                y_regression = [a * x + b for x in x_numeric]
                ax.plot(x_positions, y_regression, linewidth=1.5, color='red')
            except (ValueError, TypeError):
                pass
        
        ax.set_xlabel(question_label, fontsize=11)
        ax.set_ylabel("Nota média", fontsize=11)
        ax.grid(axis='y', alpha=0.3)

        plt.figtext(0.5, 0.02, f"f(x) = {a:.2f}x + {b:.2f}; r = {r:.2f}, r^2 = {r**2:.2f}", ha="center", color="black")
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.1)
        plt.savefig(f"./output/socioeconomic_regression/boxplot_Q{str(q_index).zfill(3)}.png", dpi=600, format="png")
        plt.close()


def main() -> None:
    socio_data = read_socioeconomic_data()
    regression(socio_data)


if __name__ == "__main__":
    main()
