from tensorflow.keras.models import model_from_json
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np

# ==========================
# Load Model
# ==========================

with open("models/model.json", "r") as json_file:
    model_json = json_file.read()

model = model_from_json(model_json)
model.load_weights("models/model.weights.h5")

print("✅ Model Loaded Successfully")

# ==========================
# Emotion Labels
# ==========================

emotion_labels = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Neutral",
    "Sad",
    "Surprise"
]

# ==========================
# Image Path
# ==========================

image_path = "images/validation/fear/21.jpg"

# ==========================
# Load and Preprocess Image
# ==========================

img = load_img(
    image_path,
    color_mode="grayscale",
    target_size=(48, 48)
)

img = img_to_array(img)
img = img / 255.0
img = np.expand_dims(img, axis=0)

# ==========================
# Predict
# ==========================

prediction = model.predict(img, verbose=0)

predicted_class = np.argmax(prediction)
predicted_emotion = emotion_labels[predicted_class]

confidence = np.max(prediction) * 100

# ==========================
# Result
# ==========================

print("\n📷 Image:", image_path)
print("😊 Predicted Emotion:", predicted_emotion)
print(f"🎯 Confidence: {confidence:.2f}%")