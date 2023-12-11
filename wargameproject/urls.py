from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from wargameapi.views import register_user, login_user, ArmyView, WargameUserView, GameView, EventView, CategoryView, SystemView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', WargameUserView, 'user')
router.register(r'armies', ArmyView, 'army')
router.register(r'games', GameView, 'game')
router.register(r'events', EventView, 'event')
router.register(r'categories', CategoryView, 'category')
router.register(r'systems', SystemView, 'system')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('', include(router.urls)),
]

