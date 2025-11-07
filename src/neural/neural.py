import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder


def read_multiple_factors() -> list[list]:
    X = []
    Y = []

    def convert_response(resp):
        if resp is None or resp == "":
            return None
        if resp.upper() in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]:
            return ord(resp.upper()) - ord("A") + 1
        try:
            return int(resp)
        except ValueError:
            return None

    print("Reading multiple factors data...")
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

            extra_fields = ["TP_FAIXA_ETARIA", "TP_SEXO", "TP_ESTADO_CIVIL", "TP_COR_RACA", "TP_NACIONALIDADE", "TP_ST_CONCLUSAO", "TP_ESCOLA", "TP_ENSINO", "IN_TREINEIRO", "CO_UF_PROVA"]
            extra_indices = [labels[field] for field in extra_fields]

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

                        for index in extra_indices:
                            if raw_vals[index] == "":
                                skip_row = True
                        
                        if not skip_row:
                            extra_vals = [0 if raw_vals[i] == 'M' else 1 if raw_vals[i] == 'F' else int(raw_vals[i]) for i in extra_indices]

                            X.append(extra_vals + socioeconomic_answers)
                            Y.append(grades)

        print(f"Read year {year}.")

    Y = [[sum(v) / len(v)] for v in Y]
    return X, Y

def train(X: list[list], Y: list[list], val_ratio=0.15, test_ratio=0.15, patience=10, lr=0.0001, num_epochs=20):
    X = np.array(X, dtype=np.float32)
    Y = np.array(Y, dtype=np.float32)

    enc = OneHotEncoder(sparse_output=False)
    X = enc.fit_transform(X)

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_trainval, X_test, Y_trainval, Y_test = train_test_split(X, Y, test_size=test_ratio, random_state=42)
    val_ratio_adjusted = val_ratio / (1 - test_ratio)
    X_train, X_val, Y_train, Y_val = train_test_split(X_trainval, Y_trainval, test_size=val_ratio_adjusted, random_state=42)

    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(X.shape[1],)),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(64, activation='relu'), 
        tf.keras.layers.Dense(units=1, activation='linear')
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
        loss='mae',
        metrics=['mae']
    )

    early_stop = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=patience,
        min_delta=1e-3,
        restore_best_weights=True
    )

    lr_scheduler = tf.keras.callbacks.ReduceLROnPlateau(
    monitor='val_loss', factor=0.5, patience=3, verbose=1
)

    history = model.fit(
        X_train, Y_train,
        validation_data=(X_val, Y_val),
        epochs=num_epochs,
        batch_size=64,  
        verbose=1,
        callbacks=[early_stop, lr_scheduler]
    )

    # ---- Evaluation on test set ----
    test_loss, test_mae = model.evaluate(X_test, Y_test, verbose=0)
    print(f"\nTest Loss: {test_loss:.4f} | Test MAE: {test_mae:.4f}")

    model.save("my_model.keras")


def main() -> None:
    X, Y = read_multiple_factors()
    train(X, Y)

if __name__ == "__main__":
    main()