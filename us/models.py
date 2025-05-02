from django.db import models
from users.models import User

class Us(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #comment = models.TextField(max_length=200)  
    #lanking = models.IntegerField(default=0)
