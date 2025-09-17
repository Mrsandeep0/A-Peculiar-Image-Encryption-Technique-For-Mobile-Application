import pickle
from PIL import Image
import os
from django.conf import settings
from skimage.io import imread
from skimage.transform import resize
import skimage

def load_image(file):
    dimension=(104, 104)
    image = Image.open(file)
    flat_data = []
    img = skimage.io.imread(file)
    img_resized = resize(img, dimension, anti_aliasing=True, mode='reflect')
    flat_data.append(img_resized.flatten())
    return image,flat_data

def user_img_process(file):

    path = os.path.join(settings.MEDIA_ROOT, 'rice_test', file)
