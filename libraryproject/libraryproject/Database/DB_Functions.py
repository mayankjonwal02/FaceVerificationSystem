from django.core.exceptions import ObjectDoesNotExist
from .UserModel import UserModel
from face_recognition import face_encodings
import numpy as np
from datetime import datetime
from django.core.cache import cache
def get_user(id):
    try:
        user = UserModel.objects.get(id=id)
        return user
    except ObjectDoesNotExist:
        return None
    
    return None

def get_all_users():
    return UserModel.objects.all()

def add_user(user):
    user.date = datetime.now()
    user.save()
    return user

def delete_user(id):
    user = get_user(id)
    if user:
        user.delete()
        return True
    return False

def update_user(user):
    user.save()
    return user


def convert_image_to_embedding(image):

    try:
        img_array = np.array(image)
        print("hello")
        embedding = face_encodings(img_array)[0]

        return embedding
    except Exception as e:
        print(e)
        return None

def get_all_embeddings():
    if cache.get("embeddings") and cache.get("user_ids"):
        print("from cache")
        return cache.get("embeddings", []), cache.get("user_ids", [])
    users = get_all_users()
    embeddings = []
    user_ids = []
    for user in users:
        for embedding in user.faceembeddings:
            embeddings.append(np.array(embedding["embedding"]))
            user_ids.append(user.id)
        
    cache.set("embeddings", embeddings,None)
    cache.set("user_ids", user_ids, None)
    return embeddings , user_ids

def updateCache():
    users = get_all_users()
    embeddings = []
    user_ids = []
    for user in users:
        for embedding in user.faceembeddings:
            embeddings.append(np.array(embedding["embedding"]))
            user_ids.append(user.id)
        
    cache.set("embeddings", embeddings,None)
    cache.set("user_ids", user_ids, None)
