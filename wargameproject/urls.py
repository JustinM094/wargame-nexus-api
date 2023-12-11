from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from wargameapi.views import register_user, login_user, ArmyView, WargameUserView, GameView, EventView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', WargameUserView, 'user')
router.register(r'armies', ArmyView, 'army')
router.register(r'games', GameView, 'game')
router.register(r'events', EventView, 'event')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('', include(router.urls)),
]

