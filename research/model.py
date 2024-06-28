import os
import time
import tensorflow as tf
import tensorflow_hub as hub

import requests
from PIL import Image
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
import numpy as np
from PIL import Image
os.environ["TFHUB_DOWNLOAD_PROGRESS"] = "True"

#step 1: upload image file to tensor flow
img = Image.open('data/input/test_images/sample_image.jpg')
lr_img = np.array(img)