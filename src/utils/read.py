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

    print("Reading socioeconomic and school type data...")
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


def convert_response(resp):

    if resp is None or resp == "":
        return None
    if resp.upper() in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", 
                        "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]:
        return ord(resp.upper()) - ord("A") + 1
    try:
        return int(resp)
    except ValueError:
        return None


def read_attendance_data(year: int) -> pd.DataFrame:
    
    file_name = f"microdados_enem_{year}/DADOS/MICRODADOS_ENEM_{year}.csv"
    
    print(f"Reading attendance data for year {year}...")
    
    with open(file_name, encoding="ISO-8859-1") as file:
        labels = file.readline().strip().replace("\n", "").split(";")
        label_to_index = {label: i for i, label in enumerate(labels)}
        
        presence_fields = ["TP_PRESENCA_CN", "TP_PRESENCA_CH", "TP_PRESENCA_LC", "TP_PRESENCA_MT"]
        presence_indices = [label_to_index[field] for field in presence_fields if field in label_to_index]
        
        socioeconomic_fields = [f"Q{str(i).zfill(3)}" for i in range(1, 26)]
        socioeconomic_indices = [label_to_index[field] for field in socioeconomic_fields if field in label_to_index]
        
        data_rows = []
        
        for row in file:
            raw_vals = row.strip().replace("\n", "").split(";")
            
            attended = False
            for idx in presence_indices:
                if idx < len(raw_vals):
                    val = raw_vals[idx]
                    if val == "1":
                        attended = True
                        break
            
            socioeconomic_answers = []
            valid_row = True
            
            for idx in socioeconomic_indices:
                if idx < len(raw_vals):
                    answer = raw_vals[idx]
                    converted = convert_response(answer)
                    socioeconomic_answers.append(converted)
                else:
                    valid_row = False
                    break
            
            if valid_row and len(socioeconomic_answers) == 25:
                non_null_count = sum(1 for ans in socioeconomic_answers if ans is not None)
                if non_null_count >= 15: 
                    row_data = socioeconomic_answers + [1 if attended else 0]
                    data_rows.append(row_data)
    
    columns = [f"Q{str(i).zfill(3)}" for i in range(1, 26)] + ["attended"]
    df = pd.DataFrame(data_rows, columns=columns)
    
    print(f"  Total samples: {len(df)}")
    print(f"  Attended: {df['attended'].sum()} ({df['attended'].mean()*100:.2f}%)")
    print(f"  Absent: {(df['attended']==0).sum()} ({(1-df['attended'].mean())*100:.2f}%)")
    
    return df


def read_error_data(year: int) -> pd.DataFrame:
    
    file_name = f"microdados_enem_{year}/DADOS/MICRODADOS_ENEM_{year}.csv"
    
    print(f"\nReading error data for year {year}...")
    print(f"File: {file_name}")
    
    with open(file_name, encoding="ISO-8859-1") as file:
        labels = file.readline().strip().replace("\n", "").split(";")
        label_to_index = {label: i for i, label in enumerate(labels)}
        
        areas = ["CN", "CH", "LC", "MT"]
        answer_indices = {}
        answer_key_indices = {}
        
        for area in areas:
            answer_field = f"TX_RESPOSTAS_{area}"
            answer_key_field = f"TX_GABARITO_{area}"
            
            if answer_field in label_to_index:
                answer_indices[area] = label_to_index[answer_field]
            if answer_key_field in label_to_index:
                answer_key_indices[area] = label_to_index[answer_key_field]
        
        print(f"Found answer fields for areas: {list(answer_indices.keys())}")
        
        error_data = []
        rows_read = 0
        rows_processed = 0
        
        for row in file:
            rows_read += 1
            
            raw_vals = row.strip().replace("\n", "").split(";")
            
            student_errors = [False] * 180
            valid_row = True
            
            for area_index, area in enumerate(areas):
                if area not in answer_indices or area not in answer_key_indices:
                    continue
                
                answers = raw_vals[answer_indices[area]]
                answer_key = raw_vals[answer_key_indices[area]]
                
                if not answers or not answer_key or answers == "" or answer_key == "":
                    valid_row = False
                    break
                
                num_questions = min(len(answers), len(answer_key), 45)
                
                for q_idx in range(num_questions):
                    if q_idx < len(answers) and q_idx < len(answer_key):
                        student_answer = answers[q_idx]
                        correct_answer = answer_key[q_idx]
                        
                        if student_answer != '.' and correct_answer != '.':
                            student_errors[area_index * 45 + q_idx] = (student_answer != correct_answer)
            
            if valid_row and len(student_errors) > 0:
                error_data.append(student_errors)
                rows_processed += 1
                
                if rows_processed % 50000 == 0:
                    print(f"  Processed {rows_processed} students...")
        
        print(f"  Total rows read: {rows_read}")
        print(f"  Valid students processed: {rows_processed}")

    df = pd.DataFrame(error_data, dtype=bool)
    
    df = df.fillna(False).astype(bool)
    
    print(f"  DataFrame shape: {df.shape}")
    print(f"  Total questions: {df.shape[1]}")
    
    return df