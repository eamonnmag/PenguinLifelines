from app.models import MediaPhoto, MediaVideo, NewsItem
from models import MultiuploaderImage, MultiUploadFolder
from django.contrib import admin



class MultiuploaderImageAdmin(admin.ModelAdmin):
    search_fields = ["filename", "key_data"]
    list_display = ["filename", "image", "key_data"]
    list_filter = ["filename", "image", "key_data"]

admin.site.register(MultiuploaderImage, MultiuploaderImageAdmin)
admin.site.register(MultiUploadFolder)
admin.site.register(MediaPhoto)
admin.site.register(MediaVideo)
admin.site.register(NewsItem)
