from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Image


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        # fields = ["author_id", 
        #           "name", 
        #           "cover",
        #           "created_at", 
        #           "updated_at"
        #         ]

        fields = '__all__'

