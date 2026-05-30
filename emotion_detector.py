from tensorflow.keras.models import model_from_json
import cv2
import numpy as np

# Load model
with open("models/model.json", "r") as json_file:
    model = model_from_json(json_file.read())

model.load_weights("models/model.weights.h5")

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

    for (x, y, w, h) in faces:

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

        prediction = model.predict(
            face,
            verbose=0
        )

        emotion = emotion_labels[
            np.argmax(prediction)
        ]

        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            emotion,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )

    cv2.imshow(
        "Emotion Detection",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()