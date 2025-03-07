
from django.conf import settings
import cv2 
import numpy as np
import os
from face_recognition import compare_faces  , face_locations
from ..Database.DB_Functions import convert_image_to_embedding
# def count_faces(image):
#     # Load the pre-trained Haar Cascade classifier for face detection
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#     # Convert PIL image to a NumPy array
#     image = np.array(image)

#     # Convert the image to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Detect faces in the image
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

#     # Count the number of faces detected
#     num_faces = len(faces)

#     return num_faces, faces


def count_faces(image):
    # Convert PIL image to a NumPy array
    image_np = np.array(image)

    # Find all face locations using the face_recognition library
    faceLocations = face_locations(image_np, model='hog')  # Use 'cnn' for better accuracy but requires GPU

    # Initialize the final list of filtered faces
    final_faces = []
    min_face_size = 130  # Minimum face size in pixels (width or height)
    max_face_size = 500  # Maximum face size in pixels (width or height)
    print(faceLocations)

    # Process detected faces and apply size filtering
    for (top, right, bottom, left) in faceLocations:
        # Calculate face width and height
        face_width = right - left
        face_height = bottom - top
        final_faces.append((left, top, face_width, face_height))
        # Check if the face meets the size criteria
        if min_face_size <= face_width <= max_face_size and min_face_size <= face_height <= max_face_size:
            
            # Draw bounding box around the face
            cv2.rectangle(image_np, (left, top), (right, bottom), (255, 0, 0), 2)

    # Sort faces in descending order of size (width × height)
    final_faces = sorted(final_faces, key=lambda face: face[2] * face[3], reverse=True)
    image_new = None
    first_face = None
    if len(final_faces) > 0:
        first_face = final_faces[0]
        image_new = image_np[first_face[1]:first_face[1] + first_face[3], first_face[0]:first_face[0] + first_face[2]]
        # print(convert_image_to_embedding(image_new))
        # cv2.imshow('Detected Faces', image_new)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
    # Display the image with bounding boxes
    # if len(final_faces) > 0:
    #     cv2.imshow('Detected Faces', image_np)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()

    # Return the count and sorted list of final faces
    return len(final_faces), first_face ,image_new


from mtcnn import MTCNN

def count_faces1(image):
    
    detector = MTCNN()

    # Convert PIL image to a NumPy array
    image_np = np.array(image)

    # Detect faces in the image
    results = detector.detect_faces(image_np)

    # Initialize list for detected faces
    faces = []

    # Draw bounding boxes and count faces
    for result in results:
        x, y, width, height = result['box']
        min_face_size = 130  # minimum width/height in pixels
        max_face_size = 400
               

        if (width > min_face_size and height > min_face_size ) and (width < max_face_size and height < max_face_size):
            faces.append((x, y, width, height))
            cv2.rectangle(image_np, (x, y), (x + width, y + height), (255, 0, 0), 2)

    # Count the number of faces detected
    num_faces = len(faces)

    # Show image if more than one face is detected
    if num_faces > 1:
        cv2.imshow('Detected Faces', image_np)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return num_faces, faces
 

def has_jpg_files():
    # Ensure the media directory exists
    if not os.path.exists(settings.MEDIA_ROOT):
        return False

    # List all files in the media directory
    all_files = os.listdir(settings.MEDIA_ROOT)

    # Check if any file ends with .jpg
    for file in all_files:
        if file.lower().endswith('.jpg'):
            return True

    return False


def recognize_face(embeddings,target_embedding):
    
    if embeddings is None or target_embedding is None:
        return -1

    if embeddings == []:
        return -1
    
    try:
        
        recognition = compare_faces(embeddings, target_embedding,tolerance=0.4)
        print(recognition)
        # check is any of the element is true then return index of first occurance of true else return -1 
        index = next((i for i, x in enumerate(recognition) if x), -1)
        return index

    except Exception as e:
        print("error from function",e)
        return -1