from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    name = models.CharField(max_length = 200)
    
    def __str__(self):
        return self.name
# Create your models here.

class Room(models.Model):
    host = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)  #when user deleted set to null
    topic = models.ForeignKey(Topic , on_delete = models.SET_NULL, null = True) #when topic deleted set to null
    name = models.CharField(max_length = 200)
    description = models.TextField(null = True, blank = True )
    participants = models.ManyToManyField(User, related_name = 'participants',blank = True)
    updated = models.DateTimeField(auto_now = True) #whenever updated it will change to curr time 
    create = models.DateTimeField(auto_now_add = True) #when created will set to curr time and not update


    class Meta:
        ordering = ['-updated', '-create']

    def __str__(self):
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)  #on deleting user delete messagess
    room = models.ForeignKey(Room, on_delete = models.CASCADE)  #on deleting room delete messages 
    body = models.TextField()
    updated = models.DateTimeField(auto_now = True)
    create = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-updated', '-create']
        
    def __str__(self):
        return self.body[0:50]
