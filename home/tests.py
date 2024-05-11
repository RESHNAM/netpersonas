from django.test import TestCase
from factory import DjangoModelFactory, Faker
from .models import *

# Create your tests here.
class ImageFactory(DjangoModelFactory):
    author = Faker('image')
    name = Faker('image')
