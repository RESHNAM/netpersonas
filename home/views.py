from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Image

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
        messages.warning(request, 'Signup first!')
        return redirect('upload')

