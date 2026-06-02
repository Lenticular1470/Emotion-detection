import base64
import os
from pathlib import Path

import cv2
import numpy as np
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from tensorflow.keras.models import model_from_json


ROOT = Path(__file__).resolve().parents[1]
MODEL_JSON = ROOT / "models" / "model.json"
MODEL_WEIGHTS = ROOT / "models" / "model.weights.h5"

EMOTION_LABELS = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Neutral",
    "Sad",
    "Surprise",
]


app = Flask(__name__, static_folder=None)
CORS(app)


def load_emotion_model():
    with MODEL_JSON.open("r", encoding="utf-8") as json_file:
        model = model_from_json(json_file.read())
    model.load_weights(str(MODEL_WEIGHTS))
    return model


model = load_emotion_model()
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def decode_data_url(data_url):
    if "," in data_url:
        data_url = data_url.split(",", 1)[1]

    image_bytes = base64.b64decode(data_url)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if frame is None:
        raise ValueError("Could not decode image.")

    return frame


def prepare_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) == 0:
        raise ValueError("No face detected.")

    x, y, w, h = max(faces, key=lambda face: face[2] * face[3])
    face = gray[y : y + h, x : x + w]
    face = cv2.resize(face, (48, 48))
    face = face.astype("float32") / 255.0
    face = np.expand_dims(face, axis=-1)
    face = np.expand_dims(face, axis=0)
    return face


@app.get("/")
def index():
    return send_from_directory(ROOT, "index.html")


@app.get("/health")
def health():
    return jsonify({"ok": True})


@app.post("/predict")
def predict():
    payload = request.get_json(silent=True) or {}
    image = payload.get("image")

    if not image:
        return jsonify({"error": "Missing image field."}), 400

    try:
        frame = decode_data_url(image)
        face = prepare_face(frame)
        prediction = model.predict(face, verbose=0)[0]
    except ValueError as exc:
        return jsonify({"error": str(exc), "faceDetected": False}), 422

    probabilities = prediction.astype(float).tolist()
    emotion_index = int(np.argmax(prediction))
    confidence = float(prediction[emotion_index] * 100)

    return jsonify(
        {
            "emotion": EMOTION_LABELS[emotion_index],
            "confidence": confidence,
            "probabilities": probabilities,
            "faceDetected": True,
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "7860"))
    app.run(host="0.0.0.0", port=port, debug=False)

    
