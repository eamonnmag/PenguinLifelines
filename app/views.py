import json
import urllib2
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from app.models import MediaVideo, MediaPhoto, NewsItem, Location
from multiuploader.models import MultiUploadFolder
from penguinlifelines import settings


def upload_home(request):
    recent_news = NewsItem.objects.order_by('-created_date')[:1]

    return render_to_response('home.html', {"news": recent_news}, context_instance=RequestContext(request))


def news(request):
    recent_news = NewsItem.objects.order_by('-created_date')
    return render_to_response('news.html', {"news": recent_news}, context_instance=RequestContext(request))


def news_item(request, newsItemId):
    newsItem = NewsItem.objects.filter(id=newsItemId)

    item = None
    if len(newsItem) > 0:
        item = newsItem.__getitem__(0)

    return render_to_response('newsItem.html', {"item": item}, context_instance=RequestContext(request))


def photos(request):
    superuser = request.user.is_authenticated and request.user.is_superuser
    photos = MediaPhoto.objects.all()
    return render_to_response('photos.html', {"photos": photos, "superuser": superuser}, context_instance=RequestContext(request))


def media(request):
    videos = MediaVideo.objects.all()
    superuser = request.user.is_superuser
    return render_to_response('media.html', {"videos": videos, "superuser": superuser}, context_instance=RequestContext(request))


@login_required()
def upload(request):
    return render_to_response('upload.html')


@login_required()
def profile(request):
    items = MultiUploadFolder.objects.filter(user=request.user)
    result = processUploadFolders(items)

    return render_to_response("profile.html",
                              {"requested_user": request.user, "items": result},
                              context_instance=RequestContext(request))


def photo_search(request):
    return render_to_response('map-search.html', context_instance=RequestContext(request))


def processUploadFolders(items):
    result = []
    for item in items:
        user = ""
        if item.user:
            user = item.user.username

        picture = None

        if len(item.files.all()) > 0:
            picture = item.files.all()[0]

        location = getHumanReadableLocation(item.latitude, item.longitude)
        result.append(
            {"id": item.uniqueIdentifier, "description": item.description, "latitude": item.latitude,
             "longitude": item.longitude,
             "human_readable_location": location, "user": user, "date": item.submissionTime,
             "picture": picture, "file_count": len(item.files.all())})
    return result


def recent_uploads(request):
    items = MultiUploadFolder.objects.all()

    result = processUploadFolders(items)
    return render_to_response('recent-uploads.html', {'items': result}, context_instance=RequestContext(request))


def folder_details(request):
    uniqueIdentifer = request.GET.get('id', None)

    items = MultiUploadFolder.objects.filter(uniqueIdentifier=uniqueIdentifer)

    item = None
    satMapURL = ""
    hybMapURL = ""
    location = ""
    if len(items) > 0:
        item = items.__getitem__(0)
        hybMapURL = "http://maps.googleapis.com/maps/api/staticmap?center=" + item.latitude + "," + item.longitude + "&size=200x200&zoom=2&maptype=terrain&sensor=true&markers=color:0xF7941E|" + item.latitude + "," + item.longitude
        satMapURL = "http://maps.googleapis.com/maps/api/staticmap?center=" + item.latitude + "," + item.longitude + "&size=200x200&maptype=satellite&sensor=true&markers=color:0xF7941E|" + item.latitude + "," + item.longitude
        location = getHumanReadableLocation(item.latitude, item.longitude)

    imagePrepender = settings.MULTI_IMAGE_URL
    return render_to_response('folder-details.html', {'item': item, 'satMap': satMapURL, 'hybMap': hybMapURL,
                                                      "human_readable_location": location,
                                                      'image_prepender': imagePrepender}, context_instance=RequestContext(request))


def getHumanReadableLocation(latitude, longitude):
    latitude_longitude = latitude + "," + longitude
    locationCacheSearch = Location.objects.filter(latlong=latitude_longitude)

    if len(locationCacheSearch) == 0:
        url = 'http://maps.googleapis.com/maps/api/geocode/json?latlng=' + latitude + ',' + longitude + '&sensor=false'
        request = urllib2.Request(url, headers={"Accept": "application/json"})
        jsonResponse = urllib2.urlopen(request).read()
        jsonResponse = json.loads(jsonResponse)

        if jsonResponse['results']:
            address = jsonResponse['results'][0]['formatted_address']
            location = Location(latlong=latitude_longitude, location=address)
            location.save()
            return address
        return "Unknown"
    else:
        return locationCacheSearch.__getitem__(0).location


@csrf_exempt
def searchUploads(request):
    north = float(request.POST.get('N', 0.0))
    west = float(request.POST.get('W', 0.0))
    east = float(request.POST.get('E', 0.0))
    south = float(request.POST.get('S', 0.0))

    items = MultiUploadFolder.objects.all()

    result = []

    for item in items:
        user = ""
        if item.user:
            user = item.user.username

        picture = None

        if len(item.files.all()) > 0:
            picture = item.files.all()[0]

        location = getHumanReadableLocation(item.latitude, item.longitude)

        if item.latitude:

            if west < float(item.longitude.strip()) < east and north > float(item.latitude.strip()) > south:
                result.append(
                    {"id": item.uniqueIdentifier, "description": item.description, "latitude": item.latitude,
                     "longitude": item.longitude,
                     "human_readable_location": location, "user": user, "date": item.submissionTime,
                     "picture": picture, "file_count": len(item.files.all())})

    return render_to_response('recent-uploads.html', {'items': result}, context_instance=RequestContext(request))


def public_profile(request, username):
    userQuery = User.objects.filter(username=username)

    requestedUser = None
    loggedInUser = False

    if len(userQuery) > 0:
        requestedUser = userQuery.get(username=username)
        loggedInUser = (requestedUser == request.user)

    items = MultiUploadFolder.objects.filter(user=requestedUser).order_by('-submissionTime')
    result = processUploadFolders(items)[:10]

    return render_to_response("profile.html",
                              {"requested_user": requestedUser, "logged_in_user": loggedInUser, "items": result},
                              context_instance=RequestContext(request))
