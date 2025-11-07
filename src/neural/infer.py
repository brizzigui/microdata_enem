from tensorflow import keras
import numpy as np

model = keras.models.load_model("my_model.keras")

sample = np.array([[1, 0.6, 25, 3.5]], dtype=np.float32)

pred = model.predict(sample)
print("Predicted output:", pred)