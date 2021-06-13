from django.db import models

# Create your models here.
class uploadfiles(models.Model):
    email=models.EmailField(max_length=255)
    phn=models.CharField(max_length=12)
    file=models.FileField(upload_to="media")
