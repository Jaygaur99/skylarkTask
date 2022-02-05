from functools import partial
from pickle import NONE
from django.shortcuts import get_object_or_404
from numpy import delete
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import viewsets

from . import models
from . import serializers
from django.contrib.auth.models import User

# Create your views here.
class GetAuthToken(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class LocationViewSet(viewsets.ModelViewSet):
    queryset = models.Location.objects.all()
    serializer_class = serializers.AddressSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )


class CameraView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk=None, *args, **kwargs):
        cameras = models.Camera.objects.filter(owner=request.user)
        if pk:
            cameras = cameras.filter(pk=pk)
        serializer = serializers.CameraSerializer(cameras, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # print(request.data)
        context = {'request': request, 'id':None}
        # print(request.data.get('location').get('id'))
        if request.data.get('location').get('id'):
            context={'request': request, 'id': request.data.get('location').get('id')}
        serializer = serializers.CameraSerializer(data=request.data, context=context)

        if serializer.is_valid():
            serializer.save(
                owner=self.request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, *args, **kwargs):
        obj = get_object_or_404(models.Camera, pk=pk)
        context = {'request': request, 'id':None}
        if request.data.get('location').get('id'):
            context={'request': request, 'id': request.data.get('location').get('id')}
        serializer = serializers.CameraSerializer(
            instance=obj, 
            data=request.data, 
            context=context, 
            partial=False
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, pk=None, *args, **kwargs):
        obj = get_object_or_404(models.Camera, pk=pk)
        context = {'request': request, 'id':None}
        if request.data.get('location').get('id'):
            context={'request': request, 'id': request.data.get('location').get('id')}
        serializer = serializers.CameraSerializer(
            instance=obj, 
            data=request.data, 
            context={'request': request}, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, reqeust, pk=None, *args, **kwargs):
        obj = get_object_or_404(models.Camera, pk=pk)
        obj.delete()
        return Response({"message": f"Camera Instance with id {pk} is deleted"}, status=status.HTTP_204_NO_CONTENT)