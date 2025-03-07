from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection
from rest_framework import status
from django.conf import settings
import os
from datetime import datetime

from django.http import JsonResponse
import shutil
from PIL import Image
import pyperclip
# import pandas as pd

from .functions.function2 import recognize_face , count_faces
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
from django.urls import reverse
from .Database import DB_Functions
from .Database import UserModel as mymodel
import threading
def developedby(request):
    return render(request, 'developedby.html')

class RegisterView(APIView):

    def get(self,request):
        user_data = DB_Functions.get_all_users()
        user_json = []
        for user in user_data:
            user_json.append({
                'id': user.id})
        return JsonResponse({'users': user_json}, status=status.HTTP_200_OK)
            


    def post(self, request):
        try:
            data = request.data
            user_id = data.get('id')
            image = request.FILES.get('image')
            imagetype = data.get('imagetype')  


            if not user_id or not image:
                return JsonResponse({'error': 'ID and image are required'}, status=status.HTTP_400_BAD_REQUEST)
            
            user_id = user_id.strip().upper()

            existing_user = DB_Functions.get_user(user_id)
            if existing_user:
                return JsonResponse({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

            
            if imagetype == 'clicked':
                multipart_data = MultipartEncoder(
                        fields={
                            'image': (image.name, image, image.content_type),
                        
                        }
                    )
                headers = {'Content-Type': multipart_data.content_type}
                internal_api_url = "http://frontalface:8001/isFront"
                response = requests.post(internal_api_url, data=multipart_data, headers=headers)
                print(response.content)
                if response.status_code == 200:
                    data = response.json()
                    print(data)
                    if data['front'] == False:
                        return JsonResponse({'error': 'Look in camera'}, status=status.HTTP_400_BAD_REQUEST)


            img =Image.open(image)
            img = img.resize((1200, 800), Image.LANCZOS)

            
            if imagetype == "clicked":
                count , face_size , face = count_faces(img)
                if(count == 0):
                    return JsonResponse({'error': 'No face found',"verified": False}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    (x, y, w, h) = face_size
            
                    
                    min_face_size = 130 
                    max_face_size = 500
                    print(x,y,w,h)
                    
                    if w < min_face_size or h < min_face_size :
                        return JsonResponse({'error': 'please stand closer to camera',"verified": False}, status=status.HTTP_400_BAD_REQUEST)
                    if w > max_face_size or h > max_face_size:
                        return JsonResponse({'error': 'please stand further from camera',"verified": False}, status=status.HTTP_400_BAD_REQUEST)
                    else :
                        img = face
                


            embeddings , user_ids = DB_Functions.get_all_embeddings()
            target_embedding = DB_Functions.convert_image_to_embedding(img)
            print("target embedding:",user_ids)
            
            recognition = recognize_face(embeddings,target_embedding)


            if recognition == -1:
                print("New Face")
                embedding = mymodel.FaceEmbedding(
                        date = datetime.now(),
                        embedding = target_embedding.tolist(),
                        embedding_id = 1
                ).to_dict()

                user = mymodel.UserModel(id=user_id, faceembeddings=[embedding])
                DB_Functions.add_user(user)
            else:
                return JsonResponse({'error': 'Face already exists'}, status=status.HTTP_400_BAD_REQUEST)

            DB_Functions.updateCache()
            return JsonResponse({'message': 'Data inserted successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:            
            return JsonResponse({'error': "There is an error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def delete(self, request):
        data = request.data
        user_id = data.get('id')


        if not user_id:
            return JsonResponse({'error': 'ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_id = user_id.strip()
        user_id = user_id.upper()

        if DB_Functions.get_user(user_id) is None:
            return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        DB_Functions.delete_user(user_id)

        DB_Functions.updateCache()
        return JsonResponse({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)


class VerifyView(APIView):
    def post(self, request):
        try:
            data = request.data
            image = request.FILES.get('image')


            if not image :
                return Response({'error': 'Image is required'}, status=status.HTTP_400_BAD_REQUEST)
            


            try:

                multipart_data = MultipartEncoder(
                    fields={
                        'image': (image.name, image, image.content_type),
                    
                    }
                )
                headers = {'Content-Type': multipart_data.content_type}
                internal_api_url = "http://frontalface:8001/isFront"
                response = requests.post(internal_api_url, data=multipart_data, headers=headers)
                print(response.content)
                if response.status_code == 200:
                    data = response.json()
                    if data['front'] == False:
                        return JsonResponse({'error': 'Look in camera'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    data = response.json()
                    return JsonResponse({'error': data['error']}, status=response.status_code)
           
            except requests.exceptions.RequestException as e:
                return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





            img = Image.open(image)
            img = img.resize((1200, 800), Image.LANCZOS)

            count , face_size , face = count_faces(img)
            if(count == 0):
                return JsonResponse({'error': 'No face found',"verified": False}, status=status.HTTP_400_BAD_REQUEST)
            else:
                (x, y, w, h) = face_size
        
                
                min_face_size = 130 
                max_face_size = 500
                print(x,y,w,h)
                
                if w < min_face_size or h < min_face_size :
                    return JsonResponse({'error': 'please stand closer to camera',"verified": False}, status=status.HTTP_400_BAD_REQUEST)
                if w > max_face_size or h > max_face_size:
                    return JsonResponse({'error': 'please stand further from camera',"verified": False}, status=status.HTTP_400_BAD_REQUEST)
                else :
                    img = face

            try:
               
                embeddings , user_ids = DB_Functions.get_all_embeddings()
                target_embedding = DB_Functions.convert_image_to_embedding(img)


                recognition = recognize_face(embeddings,target_embedding)

                if recognition == -1:
                    return JsonResponse({'message': 'Image received successfully!', 'recognition': 'Unknown',"verified": False})
                else:
                    user = DB_Functions.get_user(user_ids[recognition])
                    thread = threading.Thread(target=update_embeddings_by_user, args=(user,target_embedding))
                    thread.daemon = True
                    thread.start()
                    print("updated")
                    # update_embeddings_by_user(user,target_embedding)
                    # user_embeddings = user.faceembeddings
                    

                    return JsonResponse({'message': 'Image received successfully!', 'recognition': user_ids[recognition],"verified": True})
            except ValueError as e:
                print("error from function",e)
                return JsonResponse({'message': 'Image received successfully!', 'error': str(e), 'recognition': 'Unknown',"verified": False})

        except Exception as e:
            return Response({'error': str(e),"verified": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




def remove_data_jpg(string):

  string = os.path.basename(string)
  start_index = string.find("\\") + 1  # Skip past leading "Data/"
  end_index = string.rfind(".")  # Find the last occurrence of "."
  if start_index != -1 and end_index != -1:
    return string[start_index:end_index]
  else:
    # Handle cases where "Data/" or ".jpg" is not present
    return string
  
def update_embeddings_by_user(user : mymodel.UserModel,new_embedding):
    latestembedding = mymodel.FaceEmbedding(
        date = datetime.now(),
        embedding = new_embedding.tolist(),
    ).to_dict()
    if len(user.faceembeddings) < 3:
        try: 
            latestembedding["embedding_id"] = len(user.faceembeddings) + 1
            print("previous",len(user.faceembeddings))
            # user_embeddings = user.faceembeddings.to
            user.faceembeddings.append(latestembedding)
            print("next",len(user.faceembeddings))
            user.save()
        except Exception as e:
            print("error in if condition",e)
            return
    else:
        # update embedding for embedding id 2 or 3 based on old date 
        oldest_date = None
        oldest_index = None
        try:
           
        # Iterate over the user's faceembeddings
            for index, embedding in enumerate(user.faceembeddings):
             
                if embedding["embedding_id"] in [2, 3]:
                    # Compare dates to find the oldest embedding
                    embedding_date = embedding['date']
                    if oldest_date is None or embedding_date < oldest_date:
                        oldest_date = embedding_date
                        oldest_index = index

            if oldest_index is not None:
                old_embedding = user.faceembeddings[oldest_index]
                print(old_embedding["embedding_id"])
                user.faceembeddings[oldest_index]["embedding"] = latestembedding["embedding"]
                user.faceembeddings[oldest_index]["date"] = latestembedding["date"]
                # embedding["embedding_id"] = old_embedding["embedding_id"]

                # user.faceembeddings[oldest_index] = embedding
            user.save()
        except Exception as e:
            print("error in else condition",e)
            return 
    
    DB_Functions.updateCache()
    return 





def keep_latest_two_images( name):
    # Regular expression to match the filename pattern
    pattern = re.compile(rf'^{re.escape(name)}_(\d{{8}}\d{{6}})\.jpg$')
    
    # List to hold tuples of (timestamp, filepath)
    images = []

    folder_path = os.path.join(settings.MEDIA_ROOT)
    # Iterate over files in the folder
    for filename in os.listdir(folder_path):
        match = pattern.match(filename)
        if match:
            timestamp_str = match.group(1)
            timestamp = datetime.strptime(timestamp_str, '%Y%m%d%H%M%S')
            filepath = os.path.join(folder_path, filename)
            images.append((timestamp, filepath))
    
    # Sort images by timestamp in descending order
    images.sort(reverse=True, key=lambda x: x[0])
    
    # Keep only the latest two images and delete the rest
    for image in images[2:]:
        os.remove(image[1])



def registrationPage(request):
    return render(request, 'register.html')

def verifyPage(request):
    return render(request, 'verify.html')

def deregisterPage(request):
    pass


