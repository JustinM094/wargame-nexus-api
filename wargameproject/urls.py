from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from wargameapi.views import register_user, login_user

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('', include(router.urls)),
]

