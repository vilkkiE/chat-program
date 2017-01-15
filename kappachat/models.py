from django.db import models
from django.contrib.auth.models import User


class Channel(models.Model):
    name = models.CharField(max_length=30)


class Message(models.Model):
    content = models.TextField()
    channel = models.ForeignKey(Channel, related_name='messages')
    sentBy = models.ForeignKey(User, related_name='messages')
    created = models.DateTimeField(auto_now_add=True)