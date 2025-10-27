def read_all_grades() -> list[list]:
    data = []

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

    return data