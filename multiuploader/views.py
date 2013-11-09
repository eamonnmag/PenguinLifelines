import datetime
from django.shortcuts import get_object_or_404, render_to_response
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from models import MultiuploaderImage, MultiUploadFolder
from django.core.files.uploadedfile import UploadedFile

#importing json parser to generate jQuery plugin friendly json response
from django.utils import simplejson

#for generating thumbnails
#sorl-thumbnails must be installed and properly configured
from sorl.thumbnail import get_thumbnail

from django.views.decorators.csrf import csrf_exempt

import logging

log = logging


@csrf_exempt
def multiuploader_delete(request, pk):
    """
    View for deleting photos with multiuploader AJAX plugin.
    made from api on:
    https://github.com/blueimp/jQuery-File-Upload
    """
    if request.method == 'POST':
        log.info('Called delete image. image id=' + str(pk))
        image = get_object_or_404(MultiuploaderImage, pk=pk)
        image.delete()
        log.info('DONE. Deleted photo id=' + str(pk))
        return HttpResponse(str(pk))
    else:
        log.info('Received not POST request to delete image view')
        return HttpResponseBadRequest('Only POST accepted')


def get_or_create_image_folder(currentTime, description, latitude, longitude, request, submissionTime):
    folderQuery = MultiUploadFolder.objects.filter(uniqueIdentifier=request.user.username + currentTime)

    if len(folderQuery) > 0:
        folderItem = folderQuery.__getitem__(0)
    else:
        folderItem = MultiUploadFolder(user=request.user, uniqueIdentifier=request.user.username + currentTime,
                                       submissionTime=submissionTime, description=description, longitude=longitude,
                                       latitude=latitude)
        folderItem.save()

    return folderItem


@csrf_exempt
def multiuploader(request):
    """
    Main Multiuploader module.
    Parses data from jQuery plugin and makes database changes.
    """
    if request.method == 'POST':
        log.info('received POST to main multiuploader view')

        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')

        description = request.POST.get('description', '')
        currentTime = request.POST.get('current-time', '')
        latitude = request.POST.get('latitude', '')
        longitude = request.POST.get('longitude', '')

        print 'Description is ' + description
        print 'Submit timestamp is ' + currentTime

        # Submit timestamp is 6/10/2013 @ 10:42:27

        submissionTime = datetime.datetime.strptime(currentTime, "%d/%m/%Y @ %H:%M:%S")

        try:
            folderItem = get_or_create_image_folder(currentTime, description, latitude, longitude, request,
                                                    submissionTime)
        except Exception, e:
            print str(e)
            folderItem = get_or_create_image_folder(currentTime, description, latitude, longitude, request,
                                                    submissionTime)


        #getting file data for further manipulations
        file = request.FILES[u'files[]']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size
        log.info('Got file: "%s"' % str(filename))

        print 'File name is ' + str(filename)

        # TODO - pull out additional metadata for image.
        #writing file manually into model
        #because we don't need form of any type.
        image = MultiuploaderImage()
        image.filename = str(filename)
        image.image = file
        image.size = sizeof_fmt(file_size)
        image.key_data = image.key_generate
        image.save()
        log.info('File saving done')

        folderItem.files.add(image)

        #getting thumbnail url using sorl-thumbnail
        im = get_thumbnail(image, "80x80", quality=50)
        thumb_url = im.url

        #settings imports
        try:
            file_delete_url = settings.MULTI_FILE_DELETE_URL + '/'
            file_url = settings.MULTI_IMAGE_URL + '/' + image.key_data + '/'
        except AttributeError:
            file_delete_url = 'multi_delete/'
            file_url = 'multi_image/' + image.key_data + '/'

        #generating json response array
        result = []
        result.append({"folderitem": folderItem.uniqueIdentifier, "name": filename,
                       "size": file_size,
                       "url": file_url,
                       "thumbnail_url": thumb_url,
                       "delete_url": file_delete_url + str(image.pk) + '/',
                       "delete_type": "POST", })
        response_data = simplejson.dumps(result)

        #checking for json data type
        #big thanks to Guy Shapiro
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, mimetype=mimetype)
    else:
        return HttpResponse('Only POST accepted')


def multi_show_uploaded(request, key):
    """Simple file view helper.
    Used to show uploaded file directly"""
    image = get_object_or_404(MultiuploaderImage, key_data=key)
    url = settings.MEDIA_URL + image.image.name
    return render_to_response('multiuploader/one_image.html', {"multi_single_url": url, })


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0 and num > -1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')