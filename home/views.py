from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User, Group
from rest_framework import permissions, viewsets
from django.http import JsonResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework.generics import GenericAPIView
from rest_framework import generics

from .models import Image
from .serializers import GroupSerializer, UserSerializer, ImageSerializer

import os
import time
import json
from pathlib import Path

from urllib.request import urlretrieve

# using requests library
import requests

API_KEY = os.environ.get('API_KEY')

# Create your views here.

def index(request):

    # Page from the theme 
    #return render(request, 'pages/dashboard.html')
    return render(request, 'pages/home.html')


def upload(request):

    return render(request, 'pages/upload.html')


def detail_save(request):
    if request.method == "POST" and request.user.is_authenticated: 

        #Get Name from Request Post
        my_name = request.POST.get('myName')

        #Get Image from Request Files
        my_image = request.FILES.get('myImage')

        sys_user = User.objects.get(id=request.user.id)

        #Save the image to database
        Image.objects.create(author=sys_user, name=my_name, cover=my_image)
        messages.success(request, "Image Uploaded Successfully!")
        return redirect('upload')
    else:
        messages.warning(request, 'Signup First!')
        return redirect('upload')


def image_ai_enhance(request):
    pass

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer(queryset)
    permission_classes = [permissions.IsAuthenticated]


class NewUserList(generics.ListCreateAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer(queryset)
    permission_classes = [permissions.IsAuthenticated]


class ImageViewSet(viewsets.ModelViewSet):
    
    queryset = Image.objects.all().order_by('name')
    serializer_class = ImageSerializer(queryset)
    permission_classes = [permissions.IsAuthenticated]


class ImageListView(generics.ListCreateAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Image.objects.all().order_by('-created_at')
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = self.get_queryset()
        serializer = ImageSerializer(queryset, many=True, context={'request': request})
        # import pdb; pdb.set_trace()
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDetailView(APIView):
    """
    Retrieve, update or delete an image instance.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImageSerializer(image, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImageSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        image = self.get_object(pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

