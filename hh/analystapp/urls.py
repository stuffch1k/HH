from django.urls import path
from django.conf.urls import handler404
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

from .views import *

urlpatterns = [
    path('', index, name='home'),
]