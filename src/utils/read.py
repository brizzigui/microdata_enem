import pandas as pd

def read_all_grades() -> list[list]:
    data = []

    print("Reading data...")
    for year in range(2020, 2025):
        file_name = f"microdados_enem_{year}/DADOS/MICRODADOS_ENEM_{year}.csv" if year != 2024 else f"microdados_enem_{year}/DADOS/RESULTADOS_{year}.csv"
        
        with open(file_name, encoding="ISO-8859-1") as file:
            labels = file.readline().strip().replace("\n", "").split(";")
            labels = {label: i for i, label in enumerate(labels)}

            useful_fields = ["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]
            useful_fields = [labels[field] for field in useful_fields]

            for row in file:
                raw_vals = row.strip().replace("\n", "").split(";")
                vals = []
                for index in useful_fields:
                    if raw_vals[index] == "":
                        break

                    if not (float(raw_vals[index]) > 0):
                        break

                    vals.append(float(raw_vals[index]))
                
                else:
                    data.append(vals)

        print(f"Read year {year}.")

    return data


# this doesn't work yet!!
# reading this will be a bit more complicated...
# we need to check if the answers are right and convert them to bools and add the bools to our pd.df
# this is further complicated by the fact there are multiple test versions...
# but well get it done
def read_question_answers(year: int) -> pd.DataFrame:
    data = []

    file_name = f"microdados_enem_{year}/DADOS/MICRODADOS_ENEM_{year}.csv" if year != 2024 else f"microdados_enem_{year}/DADOS/RESULTADOS_{year}.csv"
    with open(file_name, encoding="ISO-8859-1") as file:
        labels = file.readline().strip().replace("\n", "").split(";")
        labels = {label: i for i, label in enumerate(labels)}

        useful_fields = ["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]
        useful_fields = [labels[field] for field in useful_fields]

        for row in file:
            raw_vals = row.strip().replace("\n", "").split(";")
            vals = []
            for index in useful_fields:
                if raw_vals[index] == "":
                    break

                if not (float(raw_vals[index]) > 0):
                    break

                vals.append(float(raw_vals[index]))
            
            else:
                data.append(vals)

        cols = [f'q{i}' for i in range(1, 181)]
        df = pd.DataFrame(data, columns=cols, dtype='bool')
        return df