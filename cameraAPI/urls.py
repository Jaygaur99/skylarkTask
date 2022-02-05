from urllib.parse import urlparse
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('location', views.LocationViewSet, basename='location_viewset')

urlpatterns = [
    # path('hello/', views.HelloView.as_view(), name='hello'),
    path('login/', views.GetAuthToken.as_view()),
    path('camera/', views.CameraView.as_view()),
    path('camera/<int:pk>/', views.CameraView.as_view()),
    path('', include(router.urls)),
]
