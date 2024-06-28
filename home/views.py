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
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.conf import settings
from django.templatetags.static import static

from .models import Images, Feedback
from django.contrib import messages
from .forms import FeedbackForm
from .serializers import GroupSerializer, UserSerializer, ImageSerializer

import os
import time
import requests
import json
from pathlib import Path

from urllib.request import urlretrieve

# using requests library
import requests

API_KEY = os.environ.get('API_KEY')
MEDIA_URL = settings.MEDIA_URL
MEDIA_ROOT = settings.MEDIA_ROOT
LOCALHOST = 'http://127.0.0.1:8000'
VANCE_URL = 'https://api-service.vanceai.com/web_api/v1/'

# Create your views here.
def index(request):

    # #Count number of users in the users table
    # no_of_user = User.objects.all().count()
    # print("NO OF USERS: ",no_of_user)

    # Page from the theme 
    if request.method == 'POST':
        feedb = FeedbackForm(request.POST)
        if feedb.is_valid():
            feedb.save()
            messages.add_message(request, messages.INFO, 'Contact Details Submitted Successfully!')
            return redirect('feedback')
    else:
        feedb = FeedbackForm()
    return render(request, 'pages/home.html', {'form': feedb})


def upload(request):

    return render(request, 'pages/upload-new.html')


def detail_save(request):
    if request.method == "POST" and request.user.is_authenticated: 

        #Get Name from Request Post
        my_name = request.POST.get('your-name')
        #Get Image from Request Files
        my_image = request.FILES.get('myImage')
        #Get System User
        sys_user = User.objects.get(id=request.user.id)

        #Save the image to database
        Images.objects.create(author=sys_user, name=my_name, cover=my_image)
        messages.success(request, "Image Uploaded Successfully!")

        # fetch the data and render it to the template
        active_user_image = Images.objects.filter(author=sys_user, name=my_name)

        return render(request, "pages/upload-new.html", {'active_user_image': active_user_image, 'MEDIA_URL':MEDIA_URL})
    
    elif request.method == "GET" and request.user.is_authenticated:

        # fetch the data and render it to the template
        active_user_image = Images.objects.filter(author=sys_user, name=my_name)
        context = {'active_user_image': active_user_image}

        return render(request, "pages/upload-new.html", context)
    else:
        messages.warning(request, 'Signup First!')


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
    API endpoint that allows users to be viewed or created.
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
    
class UserDetailView(APIView):
    """
    Retrieve, update or delete an user instance.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer(queryset)
    permission_classes = [permissions.IsAuthenticated]


class ImageViewSet(viewsets.ModelViewSet):
    
    queryset = Images.objects.all().order_by('name')
    serializer_class = ImageSerializer(queryset)
    permission_classes = [permissions.IsAuthenticated]


class ImageListView(generics.ListCreateAPIView):
    """
    API endpoint that allows images to be viewed or created.
    """
    queryset = Images.objects.all().order_by('-created_at')
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
            return Images.objects.get(pk=pk)
        except Images.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImageSerializer(image, context={'request': request})
        # import pdb; pdb.set_trace()
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


# class ProcessImageView(APIView):
"""
All the Process that Images are exposed to.
"""

def get_object(self, request):
    # print("ONE: ",request)
    try:
        return Images.objects.get(pk=request)
    except Images.DoesNotExist:
        raise Http404

#Denoising, deblurring and enhancing lighting 
def Denoidebluenha(request, pk):
    # print("THREE: ",pk)
    image = get_object(request, pk)
    # print("IMAGE: ",image)
    # print("IMAGEObj: ",image.cover)
    image_path = image.cover

    #Make a call to deep ai endpoint
    headers = {
        'x-api-key': API_KEY,
    }

    data = {
        "enhancements": ["denoise", "deblur", "light"],
        "width": 2000
    }

    data_dumped = {"parameters": json.dumps(data)}

    response = requests.post('https://deep-image.ai/rest_api/process_result', headers=headers, files={'image': image_path},
                data=data_dumped)
    
    print("DEEP-RESPONSE: ",response)

    print("DEEP-RESPONSE: ",response.json())

    
    if response.status_code == 200:
        response_json = response.json()
        if response_json.get('status') == 'complete':
            p = Path(response_json['result_url'])
            final_object=urlretrieve(response_json['result_url'], p.name)
            final_object_url=response_json['result_url']
            print("DEEP-RESPONSE-obj: ",final_object)
            print("DEEP-RESPONSE-url: ",final_object_url)
        elif response_json['status'] in ['received', 'in_progress']:
            while response_json['status'] == 'in_progress':
                response = requests.get(f'https://deep-image.ai/rest_api/result/{response_json["job"]}',
                            headers=headers)
                response_json = response.json()
                time.sleep(1)
            if response_json['status'] == 'complete':
                p = Path(response_json['result_url'])
                final_object=urlretrieve(response_json['result_url'], p.name)
                print("DEEP-RESPONSE-obj: ",final_object)
                print("DEEP-RESPONSE-url: ",final_object_url)

    return response.json()


def feedback(request):
    if request.method == 'POST':
        feedb = FeedbackForm(request.POST)
        if feedb.is_valid():
            feedb.save()
            messages.add_message(request, messages.INFO, 'Contact Details Submitted Successfully!')
            return redirect('feedback')
    else:
        feedb = FeedbackForm()
    return render(request, 'pages/feedback.html', {'form': feedb})


def get_all_logged_in_users():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
    uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    print("CONFIRM: ",User.objects.filter(id__in=uid_list))
    return User.objects.filter(id__in=uid_list)


# AI Libraries

import os
import time
from PIL import Image
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
os.environ["TFHUB_DOWNLOAD_PROGRESS"] = "True"


def preprocess_image(image_path):
    """ Loads image from path and preprocesses to make it model ready
      Args:
        image_path: Path to the image file
    """
    #hr_image = tf.image.decode_image(tf.io.read_file(image_path))
    hr_image = np.asarray(image_path)
    # If PNG, remove the alpha channel. The model only supports
    # images with 3 color channels.
    if hr_image.shape[-1] == 4:
        hr_image = hr_image[...,:-1]
    hr_size = (tf.convert_to_tensor(hr_image.shape[:-1]) // 4) * 4
    hr_image = tf.image.crop_to_bounding_box(hr_image, 0, 0, hr_size[0], hr_size[1])
    hr_image = tf.cast(hr_image, tf.float32)
    print("HR IMAGE PREPROCESS: ", hr_image)

    return tf.expand_dims(hr_image, 0)

def save_image(image, filename):
    """
    Saves unscaled Tensor Images.
    Args:
      image: 3D image tensor. [height, width, channels]
      filename: Name of the file to save.
    """
    if not isinstance(image, Image.Image):
        image = tf.clip_by_value(image, 0, 255)
        image = Image.fromarray(tf.cast(image, tf.uint8).numpy())
    image.save(filename)
    # print("Saved as %s.jpg" % filename)


def plot_image(image, title):
    """
    Plots images from image tensors.
    Args:
      image: 3D image tensor. [height, width, channels].
      title: Title to display in the plot.
    """
    image = np.asarray(image)
    image = tf.clip_by_value(image, 0, 255)
    image = Image.fromarray(tf.cast(image, tf.uint8).numpy())
    plt.imshow(image)
    plt.axis("off")
    plt.title(title)


# Defining helper functions
def downscale_image(image):
    """
        Scales down images using bicubic downsampling.
        Args:
            image: 3D or 4D tensor of preprocessed image
    """
    image_size = []
    if len(image.shape) == 3:
        image_size = [image.shape[1], image.shape[0]]
    else:
        raise ValueError("Dimension mismatch. Can work only on single image.")

    image = tf.squeeze(
        tf.cast(
            tf.clip_by_value(image, 0, 255), tf.uint8))

    lr_image = np.asarray(
        Image.fromarray(image.numpy())
        .resize([image_size[0] // 4, image_size[1] // 4],
        Image.BICUBIC))

    lr_image = tf.expand_dims(lr_image, 0)
    lr_image = tf.cast(lr_image, tf.float32)
    return lr_image


def ai_image_process(request, pk):
    image = get_object(request, pk)
    image_path = os.path.join(MEDIA_ROOT + '/' + str(image.cover))
    SAVED_MODEL_PATH = os.path.join(MEDIA_ROOT + '/' + "tensorflow")
    print("SAVED MODEL PATH: ",SAVED_MODEL_PATH)
  
    img = Image.open(image_path)

    hr_image = preprocess_image(img)

    # Plotting Original Resolution image
    plot_image(tf.squeeze(hr_image), title=str(image.cover))
    print("PLOT IMAGE: ", plot_image)
    save_image(tf.squeeze(hr_image), filename=image_path)
    print("SAVE IMAGE: ", save_image)

    model = hub.load(SAVED_MODEL_PATH)
    start = time.time()
    fake_image = model(hr_image)
    fake_image = tf.squeeze(fake_image)
    print("Time Taken: %f" % (time.time() - start))

    # Plotting Super Resolution Image
    plot_image(tf.squeeze(fake_image), title="Super Resolution" + " " + str(image.cover))
    save_image(tf.squeeze(fake_image), filename="Super Resolution" + " " + str(image.cover))

    

