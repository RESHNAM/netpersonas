from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Images


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ImageSerializer(serializers.Serializer):
    author = UserSerializer()
    name = serializers.CharField(max_length=200)
    cover = serializers.ImageField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
