from tensorflow.keras.models import model_from_json

# Load architecture
with open("models/model.json", "r") as json_file:
    loaded_model_json = json_file.read()

model = model_from_json(loaded_model_json)

# Load weights
model.load_weights("models/model.weights.h5")

print("Model Loaded Successfully")