from djongo import models

class FaceEmbedding(models.Model):
    date = models.DateTimeField()  # To store the date
    embedding = models.JSONField()  # To store the embedding array
    embedding_id = models.IntegerField()

    def to_dict(self):
        return {
            'date': self.date,
            'embedding': self.embedding,
            'embedding_id': self.embedding_id
        }
    
    class Meta:
        abstract = True  # Marks this as an embedded model

class UserModel(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    faceembeddings = models.ArrayField(
        model_container=FaceEmbedding
    )
