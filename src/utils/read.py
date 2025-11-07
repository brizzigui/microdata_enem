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


def read_error_data(year: int, max_rows: int = None, return_mapping: bool = False):

    file_name = f"microdados_enem_{year}/DADOS/MICRODADOS_ENEM_{year}.csv"

    print(f"\nReading error data for year {year}...")
    print(f"File: {file_name}")

    items_file = f"microdados_enem_{year}/DADOS/ITENS_PROVA_{year}.csv"
    try:
        items_df = pd.read_csv(items_file, sep=';', encoding='ISO-8859-1', dtype=str, low_memory=False)
        for col in ['CO_POSICAO', 'SG_AREA', 'CO_ITEM', 'TX_GABARITO', 'TX_COR', 'CO_PROVA']:
            if col not in items_df.columns:
                raise KeyError(f"Missing column {col} in {items_file}")
    except Exception as e:
        print(f"  Warning: could not read items file ({items_file}) - will use position-based mapping. Error: {e}")
        items_df = None

    areas = ['CN', 'CH', 'LC', 'MT']
    per_area_provas = [[] for _ in range(4)]  
    canonical_order = [[] for _ in range(4)]

    if items_df is not None:
        items_df['CO_POSICAO'] = items_df['CO_POSICAO'].astype(int)
        for area_index, area in enumerate(areas):
            df_area = items_df[items_df['SG_AREA'] == area]
            if df_area.empty:
                continue

            for co_prova, grp in df_area.groupby('CO_PROVA'):
                grp_sorted = grp.sort_values('CO_POSICAO')
                items_list = list(grp_sorted['CO_ITEM'].astype(str))
                key_list = list(grp_sorted['TX_GABARITO'].astype(str).fillna('.'))
                key_str = ''.join(key_list)
                per_area_provas[area_index].append((str(co_prova), items_list, key_str))

            try:
                df_ref = df_area[df_area['TX_COR'].str.upper().str.contains('BRAN')]
                if not df_ref.empty:
                    ref_prova = df_ref['CO_PROVA'].iloc[0]
                else:
                    ref_prova = df_area['CO_PROVA'].mode().iloc[0]

                ref_grp = df_area[df_area['CO_PROVA'] == ref_prova].sort_values('CO_POSICAO')
                canonical_order[area_index] = list(ref_grp['CO_ITEM'].astype(str))
            except Exception:
                canonical_order[area_index] = []

    with open(file_name, encoding='ISO-8859-1') as file:
        labels = file.readline().strip().replace('\n', '').split(';')

        answer_indices = [None] * 4
        answer_key_indices = [None] * 4
        for i, area in enumerate(areas):
            ans_field = f"TX_RESPOSTAS_{area}"
            key_field = f"TX_GABARITO_{area}"
            try:
                answer_indices[i] = labels.index(ans_field)
            except ValueError:
                answer_indices[i] = None
            try:
                answer_key_indices[i] = labels.index(key_field)
            except ValueError:
                answer_key_indices[i] = None

        present_areas = [areas[i] for i in range(4) if answer_indices[i] is not None and answer_key_indices[i] is not None]
        print(f"Found answer fields for areas: {present_areas}")

        error_data = []
        rows_read = 0
        rows_processed = 0

        for row in file:
            rows_read += 1
            if max_rows is not None and rows_read > max_rows:
                break

            raw_vals = row.strip().replace('\n', '').split(';')
            student_errors = [False] * 180
            valid_row = True

            for area_index in range(4):
                ai = answer_indices[area_index]
                aki = answer_key_indices[area_index]
                if ai is None or aki is None:
                    continue

                if ai >= len(raw_vals) or aki >= len(raw_vals):
                    valid_row = False
                    break

                answers = raw_vals[ai]
                answer_key = raw_vals[aki]
                if not answers or not answer_key:
                    valid_row = False
                    break

                mapped_items = None
                if items_df is not None and per_area_provas[area_index]:
                    for co_prova, items_list, key_str in per_area_provas[area_index]:
                        if key_str == answer_key:
                            mapped_items = items_list
                            break

                num_questions = min(len(answers), len(answer_key), 45)

                if mapped_items is not None:
                    for q_idx in range(num_questions):
                        if q_idx >= len(answers) or q_idx >= len(answer_key):
                            break
                        student_answer = answers[q_idx]
                        correct_answer = answer_key[q_idx]
                        if student_answer != '.' and correct_answer != '.':
                            co_item = mapped_items[q_idx] if q_idx < len(mapped_items) else None
                            if co_item is None:
                                global_pos = area_index * 45 + q_idx
                            else:
                                try:
                                    canonical_pos = canonical_order[area_index].index(co_item)
                                    global_pos = area_index * 45 + canonical_pos
                                except ValueError:
                                    # fallback to positional
                                    global_pos = area_index * 45 + q_idx

                            if 0 <= global_pos < 180:
                                student_errors[global_pos] = (student_answer != correct_answer)
                else:
                    # fallback: assume positions align
                    for q_idx in range(num_questions):
                        if q_idx >= len(answers) or q_idx >= len(answer_key):
                            break
                        student_answer = answers[q_idx]
                        correct_answer = answer_key[q_idx]
                        if student_answer != '.' and correct_answer != '.':
                            student_errors[area_index * 45 + q_idx] = (student_answer != correct_answer)

            if valid_row:
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

    col_mapping = []
    for area_index, area in enumerate(areas):
        area_items = canonical_order[area_index]
        for item in area_items:
            col_mapping.append(f"{area}_{item}")
        if len(area_items) < 45:
            for i in range(len(area_items), 45):
                col_mapping.append(f"{area}_pos{i}")

    if len(col_mapping) > df.shape[1]:
        col_mapping = col_mapping[:df.shape[1]]
    elif len(col_mapping) < df.shape[1]:
        for i in range(len(col_mapping), df.shape[1]):
            col_mapping.append(f"idx_{i}")

    if return_mapping:
        return df, col_mapping
    return df