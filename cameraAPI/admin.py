from django.contrib import admin
from .models import Camera, Location

# Register your models here.
@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ('label', 'location', 'owner', 'stream_url')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('label', 'street_address', 'city', 'state', 'country', 'latitude', 'longitude')