from django.db import models

# Create your models here.
class Insta_rating(models.Model):
        email = models.CharField(max_length=200, null=True)
        pic1 = models.CharField(max_length=200, null=True)
        pic2 = models.CharField(max_length=200, null=True)	
        pic3 = models.CharField(max_length=200, null=True)
        pic4 = models.CharField(max_length=200, null=True)
        pic5 = models.CharField(max_length=200, null=True)
        pic6 = models.CharField(max_length=200, null=True)		
    