from django.urls import path
from . import views
urlpatterns = [
    path('', views.input,name='input'),
    path('upload',views.upload,name='upload'),
    path('output',views.output,name='output'),
    path('download',views.download,name='download')
]
