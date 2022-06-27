from django.urls import path
from . import views

urlpatterns = [
    path('uploadImage/', views.process_image, name='upload'),
    path('', views.index, name='index'),
]