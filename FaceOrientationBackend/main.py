from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
import cv2
import io
import mediapipe as mp

app = FastAPI()

def is_face_front_center(image):
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    if image is None:
        return False

    # Convert the BGR image to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and find faces
    results = face_mesh.process(rgb_image)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Get specific landmarks
            nose_tip = face_landmarks.landmark[4]
            left_eye = face_landmarks.landmark[33]
            right_eye = face_landmarks.landmark[263]
            left_mouth = face_landmarks.landmark[61]
            right_mouth = face_landmarks.landmark[291]

            # Calculate face direction
            horizontal_direction = ""
            vertical_direction = ""
            
            # Check horizontal direction
            eye_distance = right_eye.x - left_eye.x
            nose_to_left = nose_tip.x - left_eye.x
            nose_to_right = right_eye.x - nose_tip.x
            
            if nose_to_left < 0.45 * eye_distance:
                horizontal_direction = "Left"
            elif nose_to_right < 0.45 * eye_distance:
                horizontal_direction = "Right"
            else:
                horizontal_direction = "Front"

            # Check vertical direction
            eye_y = (left_eye.y + right_eye.y) / 2
            mouth_y = (left_mouth.y + right_mouth.y) / 2
            vertical_range = mouth_y - eye_y
            
            if nose_tip.y < eye_y + 0.15 * vertical_range:
                vertical_direction = "Up"
            elif nose_tip.y > mouth_y - 0.15 * vertical_range:
                vertical_direction = "Down"
            else:
                vertical_direction = "Center"

            face_direction = f"{horizontal_direction} {vertical_direction}"

            # Return True if face direction is "Front Center", False otherwise
            return face_direction == "Front Center"

    # If no face is detected, return False
    return False

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/isFront")
async def is_front(image: UploadFile = File(...)):
    try:
        # Read the image file
        image_data = await image.read()

        # Open the image using PIL
        img = Image.open(io.BytesIO(image_data))

        # Convert the PIL image to a NumPy array
        img = np.array(img)

        # Convert RGB to BGR for OpenCV if the image is in RGB format
        if img.ndim == 3 and img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Check if the face is front and center
        is_front = is_face_front_center(img)
        return JSONResponse(content={"front": is_front}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
