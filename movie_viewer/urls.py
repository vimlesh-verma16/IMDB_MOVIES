from . import views
from django.urls import path,include

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_csv, name='upload-csv'),
    path('movies/', views.movie_list, name='movie-list'),
]