from UserModel import UserModel, FaceEmbedding
from datetime import datetime
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'libraryproject.settings')
django.setup()

# Create a user with embeddings
embedding1 = FaceEmbedding(date=datetime.now(), embedding=[0.1, 0.2, 0.3] , embedding_id=1)
user = UserModel(id="12345", faceembeddings=[embedding1])
user.save()

# Query the user
user = UserModel.objects.get(id="12345")
print(user.faceembeddings)
