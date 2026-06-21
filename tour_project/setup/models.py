# Create your models here.
from django.db import models


class UserTokens(models.Model):
    email = models.EmailField(max_length=255)
    token = models.UUIDField(max_length=255)
