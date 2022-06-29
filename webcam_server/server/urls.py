from django.urls import path
from . import views

urlpatterns = [
    path('uploadImage/', views.process_image, name='upload'),
    path('uploadAadhaar/', views.get_with_aadhaar, name='aadhaar'),
    path('saveDetails/', views.add_data, name='saveDetails'),
    path('', views.index, name='index'),
]