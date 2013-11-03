"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

class Test(TestCase):
    def compareLatLong(self):

        north = 54.470037612805754
        south = 46.922499263758255
        west = -6.6796875
        east = 5.09765625

        latitude = "47.75099230000001"
        longitude = "-1.2648815"

        assert west < float(longitude) < east and north > float(latitude) > south