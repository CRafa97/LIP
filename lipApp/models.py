from django.db import models
from lip import LIPImage
import os

# Create your models here.
class AppImage(object):
    def __init__(self, name, folder):
        self.sfolder = 'static/' + folder
        self.img = LIPImage.from_file(self.sfolder + name)
        self.name = name
        self.folder = folder # Folder

    @property
    def paths(self):
        return { img.split('.')[0]:img for img in os.listdir(self.sfolder) }