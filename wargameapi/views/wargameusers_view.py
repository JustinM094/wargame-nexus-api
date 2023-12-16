from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from wargameapi.models import WargameUser, EventGamer, Event

# class EventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model: Event



class WargameUserView(ViewSet):

    def retrieve(self, request, pk=None):
        wargame_user = WargameUser.objects.get(pk=pk)
        serialized = WargameUserSerializer(wargame_user)
        return Response(serialized.data)
    
    def list(self, request):
        wargame_users = WargameUser.objects.all()
        serialized = WargameUserSerializer(wargame_users, many=True)
        return Response(serialized.data)
    
class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()


    def get_first_name(self, obj):
        return f'{obj.first_name}'
    
    def get_last_name(self, obj):
        return f'{obj.last_name}'
    
    def get_email(self, obj):
        return f'{obj.email}'
    
    def get_username(self, obj):
        return f'{obj.username}'


    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username',)

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id',)

class EventGamerSerializer(serializers.ModelSerializer):
    event = EventSerializer(many=False)
    class Meta:
        model = EventGamer
        fields = ('id', 'event',)
    

class WargameUserSerializer(serializers.ModelSerializer):  
    gamer_events = EventGamerSerializer(many=True)
    user = UserSerializer(many=False)

    class Meta:
        model = WargameUser
        fields = ('id', 'bio', 'profile_image_url', 'user', 'gamer_events')