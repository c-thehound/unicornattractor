from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class User(AbstractUser):
    
    def __str__(self):
        return self.username
    
@receiver(post_save, sender=User)
def create_token(sender, instance,created, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Technician(User):

    def __str__(self):
        return self.username