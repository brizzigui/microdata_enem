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
    

def read_socioeconomic_data() -> list[list]:
    data = []

    def convert_response(resp):
        if resp is None or resp == "":
            return None
        if resp.upper() in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]:
            return ord(resp.upper()) - ord("A") + 1
        try:
            return int(resp)
        except ValueError:
            return None

    print("Reading socioeconomic data...")
    for year in range(2020, 2024):
        if year == 2022:
            continue

        file_name = f"microdados_enem_{year}/DADOS/MICRODADOS_ENEM_{year}.csv"
        
        with open(file_name, encoding="ISO-8859-1") as file:
            labels = file.readline().strip().replace("\n", "").split(";")
            labels = {label: i for i, label in enumerate(labels)}

            grade_fields = ["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]
            grade_indices = [labels[field] for field in grade_fields]

            socioeconomic_fields = [f"Q{str(i).zfill(3)}" for i in range(1, 26)]
            socioeconomic_indices = [labels[field] for field in socioeconomic_fields]

            for row in file:
                raw_vals = row.strip().replace("\n", "").split(";")

                grades = []
                for index in grade_indices:
                    if raw_vals[index] == "":
                        break

                    try:
                        grade = float(raw_vals[index])
                        if not (grade > 0):
                            break
                        grades.append(grade)
                    except ValueError:
                        break
                
                else:
                    if len(grades) == 5:
                        avg_grade = sum(grades) / len(grades)

                        socioeconomic_answers = []

                        skip_row = False 

                        for i, index in enumerate(socioeconomic_indices):
                            answer = raw_vals[index] if raw_vals[index] != "" else None
                            converted = convert_response(answer)

                            if i < 4 and converted is not None:
                                if (i < 2 and converted == 8) or (i >= 2 and converted == 6):
                                    skip_row = True
                                    break

                            socioeconomic_answers.append(converted)

                        if not skip_row:
                            data.append([avg_grade] + socioeconomic_answers)

        print(f"Read year {year}.")

    return data

def read_socioeconomic_data_school_type() -> list[list]:
    data = []

    def convert_response(resp):
        if resp is None or resp == "":
            return None
        if resp.upper() in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]:
            return ord(resp.upper()) - ord("A") + 1
        try:
            return int(resp)
        except ValueError:
            return None

    print("Reading socioeconomic data...")
    for year in range(2020, 2024):
        if year == 2022:
            continue

        file_name = f"microdados_enem_{year}/DADOS/MICRODADOS_ENEM_{year}.csv"
        
        with open(file_name, encoding="ISO-8859-1") as file:
            labels = file.readline().strip().replace("\n", "").split(";")
            labels = {label: i for i, label in enumerate(labels)}

            grade_fields = ["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]
            grade_indices = [labels[field] for field in grade_fields]

            socioeconomic_fields = [f"Q{str(i).zfill(3)}" for i in range(1, 26)]
            socioeconomic_indices = [labels[field] for field in socioeconomic_fields]

            school_type_field = "TP_DEPENDENCIA_ADM_ESC"
            school_type_index = labels[school_type_field]

            for row in file:
                raw_vals = row.strip().replace("\n", "").split(";")

                if raw_vals[school_type_index] == "":
                    continue

                grades = []
                for index in grade_indices:
                    if raw_vals[index] == "":
                        break

                    try:
                        grade = float(raw_vals[index])
                        if not (grade > 0):
                            break
                        grades.append(grade)
                    except ValueError:
                        break
                
                else:
                    if len(grades) == 5:
                        socioeconomic_answers = []

                        skip_row = False 

                        for i, index in enumerate(socioeconomic_indices):
                            answer = raw_vals[index] if raw_vals[index] != "" else None
                            converted = convert_response(answer)

                            if i < 4 and converted is not None:
                                if (i < 2 and converted == 8) or (i >= 2 and converted == 6):
                                    skip_row = True
                                    break

                            socioeconomic_answers.append(converted)

                        if not skip_row:
                            data.append([int(raw_vals[school_type_index])] + socioeconomic_answers)

        print(f"Read year {year}.")

    return data

def read_uf_grades_type() -> list[list]:
    data = []

    print("Reading data...")
    for year in range(2020, 2025):
        file_name = f"microdados_enem_{year}/DADOS/MICRODADOS_ENEM_{year}.csv" if year != 2024 else f"microdados_enem_{year}/DADOS/RESULTADOS_{year}.csv"
        
        with open(file_name, encoding="ISO-8859-1") as file:
            labels = file.readline().strip().replace("\n", "").split(";")
            labels = {label: i for i, label in enumerate(labels)}

            useful_fields = ["TP_DEPENDENCIA_ADM_ESC", "SG_UF_ESC", "NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]
            useful_fields = [labels[field] for field in useful_fields]

            for row in file:
                raw_vals = row.strip().replace("\n", "").split(";")
                vals = []
                for i, index in enumerate(useful_fields):
                    if raw_vals[index] == "":
                        break
                    
                    if i > 1:
                        if not (float(raw_vals[index]) > 0):
                            break

                        vals.append(float(raw_vals[index]))
                    
                    else:
                        vals.append(raw_vals[index])

                
                else:
                    data.append(vals)

        print(f"Read year {year}.")

    return data