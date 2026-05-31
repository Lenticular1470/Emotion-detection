from tensorflow.keras.models import model_from_json
import cv2
import numpy as np
import time

# Load model
with open("models/model.json", "r") as json_file:
    model = model_from_json(json_file.read())

model.load_weights("models/model.weights.h5")

# Emotion labels
emotion_labels = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Neutral",
    "Sad",
    "Surprise"
]

# Face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# Webcam
cap = cv2.VideoCapture(0)

# Variables for stable prediction
last_prediction_time = 0
current_emotion = "Detecting..."
current_confidence = 0

while True:

    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    # Face count
    cv2.putText(
        frame,
        f"Detected Faces: {len(faces)}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    for (x, y, w, h) in faces:

        # Extract face
        face = gray[y:y+h, x:x+w]

        face = cv2.resize(
            face,
            (48, 48)
        )

        face = face.astype("float32") / 255.0

        face = np.expand_dims(
            face,
            axis=-1
        )

        face = np.expand_dims(
            face,
            axis=0
        )

        current_time = time.time()

        # Predict only once every second
        if current_time - last_prediction_time >= 1:

            prediction = model.predict(
                face,
                verbose=0
            )

            emotion_index = np.argmax(
                prediction
            )

            current_emotion = emotion_labels[
                emotion_index
            ]

            current_confidence = (
                np.max(prediction) * 100
            )

            last_prediction_time = current_time

        label = (
            f"{current_emotion} "
            f"({current_confidence:.2f}%)"
        )

        # Color based on confidence
        if current_confidence > 90:
            color = (0, 255, 0)

        elif current_confidence > 70:
            color = (0, 255, 255)

        else:
            color = (0, 0, 255)

        # Draw face box
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            color,
            2
        )

        # Draw emotion label
        cv2.putText(
            frame,
            label,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

    cv2.imshow(
        "Real-Time Emotion Detection",
        frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()