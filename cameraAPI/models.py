from this import d
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.


class Camera(models.Model):
    location = models.ForeignKey('Location', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    thumbnail = models.URLField(blank=True)
    stream_url = models.CharField(max_length=512)
    
    @property
    def get_location(self):
        return self.location.label

    def update_thumbnail(self, path):
        self.thumbnail = path
        self.save()

    def __str__(self):
        return self.get_location + ' - ' + self.label

    def clean_url(self):
        if not self.stream_url.startswith('rtsp://'):
            raise ValidationError('Stream URL must start with rtsp://')

    def save(self, *args, **kwargs):
        self.clean_url()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('owner', )
    
    
class Location(models.Model):
    label = models.CharField(max_length=100)
    street_address = models.CharField(max_length=256)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=22, decimal_places=16)
    longitude = models.DecimalField(max_digits=22, decimal_places=16)

    def __str__(self):
        return self.label + '-' + self.city

    class Meta:
        ordering = ('city', )
