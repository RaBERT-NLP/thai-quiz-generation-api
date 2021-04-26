from django.db import models

# Create your models here.
class QACahce(models.Model):
    text = models.CharField(max_length=100)
    text_hash = models.CharField(max_length=12,default="none")
    question = models.CharField(max_length=255,default="none")
    answer = models.CharField(max_length=60)
    choices = models.CharField(max_length=255,default="none")

def __str__(self):
        return self.answer