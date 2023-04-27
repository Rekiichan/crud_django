from django.db.models import fields
from rest_framework import serializers

from .models import Item
from django.contrib.auth.models import User
 
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('category', 'subcategory', 'name', 'amount', 'user')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['password', 'is_superuser']

