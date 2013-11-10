from penguinlifelines import settings
from django.db import models

__author__ = 'eamonnmaguire'

try:
    storage = settings.MULTI_IMAGES_FOLDER + '/'
except AttributeError:
    storage = 'multiuploader_images/'



class MediaPhoto(models.Model):
    """Model for storing photo items"""
    name = models.CharField(max_length=60, blank=True, null=True)
    imageFile = models.FileField(upload_to=storage, blank=True)
    imageURL = models.URLField(blank=True)
    description = models.TextField(default="", blank=True)

    upload_date = models.DateTimeField(auto_now_add=True, blank=True)

    def __unicode__(self):
        return self.name


class MediaVideo(models.Model):
    """Model for storing video items"""
    name = models.CharField(max_length=60, blank=True, null=True)
    videoURL = models.URLField(default="")
    description = models.TextField(default="", blank=True)

    upload_date = models.DateTimeField(auto_now_add=True, blank=True)

    def __unicode__(self):
        return self.name


class NewsItem(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True, blank=True)

    def __unicode__(self):
        return self.title


class Location(models.Model):
    latlong = models.CharField(max_length=128)
    location = models.CharField(max_length=128)

    def __unicode__(self):
        return self.location
