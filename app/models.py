from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

class Item(models.Model):
    uuid = models.UUIDField(max_length=40, primary_key=True, auto_created=True, default=uuid4())
    category = models.CharField(max_length=255)
    subcategory = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
 
    def __str__(self) -> str:
        return self.name

