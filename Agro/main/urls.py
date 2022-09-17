from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('', views.about1, name='about1'),
    path('about', views.about2, name='about2')
]
