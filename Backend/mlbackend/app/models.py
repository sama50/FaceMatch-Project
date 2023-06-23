from django.db import models

# Create your models here.

class SaveImage(models.Model):
    comeing_img = models.ImageField(upload_to='media', blank=True)
    output_img = models.ImageField(upload_to='media', blank=True)