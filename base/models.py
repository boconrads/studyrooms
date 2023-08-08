from django.db import models
from django.contrib.auth.models import User # import default user models, see official django documentation

# Create your models here.

class Topic (models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # Access user that we imported above. someone has to host the room
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) # Access topic defined in class above
    name = models.CharField(max_length=200) #name of room
    description = models.TextField(null=True, blank=True) #room description, is optional
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True) #takes timestamp everytime you save it
    created = models.DateTimeField(auto_now_add=True) #takes timestamp when created

    class Meta:
        ordering = ['-updated', '-created'] #dash means descending order, so reversed ordering

    def __str__(self):
        return self.name
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE) #connect to db, when room is deleted, cascade (delete all children)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) 
    created = models.DateTimeField(auto_now_add=True) 

    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.body[0:50]
