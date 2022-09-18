from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('findVino', views.findvino, name='findVino'),
    path('res', views.res, name='result'),
    path('', views.about1, name='about1'),
    path('about', views.about2, name='about2')
]
