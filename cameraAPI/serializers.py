from django.shortcuts import get_object_or_404
from rest_framework import serializers
from . import models


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Location
        fields = ('id', 'label', 'street_address', 'city', 'state', 'country', 'latitude', 'longitude')

    def create(self, validated_data, id=None):
        # print(id)
        if id:
            address = get_object_or_404(models.Location, id=int(id))
        else:
            address = models.Location.objects.create(
                label=validated_data['label'],
                street_address=validated_data['street_address'],
                city=validated_data['city'],
                state=validated_data['state'],
                country=validated_data['country'],
                latitude=validated_data['latitude'],
                longitude=validated_data['longitude']
            )  
        return address

class CameraSerializer(serializers.Serializer):
    label = serializers.CharField(max_length=100)
    description = serializers.CharField()
    stream_url = serializers.CharField(max_length=512)
    location = AddressSerializer(many=False)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        location = validated_data['location']
        loc = AddressSerializer.create(AddressSerializer(), location, self.context['id'])

        camera = models.Camera.objects.create(
            label=validated_data['label'],
            description=validated_data['description'],
            stream_url=validated_data['stream_url'],
            location=loc,
            owner=self.context['request'].user,
        )
        return camera

    def update(self, instance, validated_data):
        if validated_data.get('location', instance.location):
            location = validated_data.get('location', instance.location)
            if not location == instance.location:
                loc = AddressSerializer.create(AddressSerializer(), location, self.context['id'])
                instance.location = loc
            else:
                instance.location = location
        instance.label = validated_data.get('label', instance.label)
        instance.description = validated_data.get('description', instance.description)
        instance.stream_url = validated_data.get('stream_url', instance.stream_url)
        instance.save()
        return instance