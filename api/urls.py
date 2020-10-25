from .views import lyric, search, detail
from django.urls import path
from . import views

urlpatterns = [
    path('lyrics/', views.lyric, name='song-list'),
    path('search/', views.search, name='Search'),
    path('lyrics/<str:pk>/', views.detail, name='Lyrics')
]
