from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from wargameapi.models import WargameUser, EventGamer, Event

# class EventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model: Event

class WargameUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WargameUser
        fields = ('id', 'bio', 'profile_image_url', 'user', 'gamer_events', 'wargame_username')

class WargameUserView(ViewSet):

    def retrieve(self, request, pk=None):
        wargame_user = WargameUser.objects.get(pk=pk)
        serialized = WargameUserSerializer(wargame_user)
        return Response(serialized.data)
    
    def list(self, request):
        wargame_users = WargameUser.objects.all()
        serialized = WargameUserSerializer(wargame_users, many=True)
        return Response(serialized.data)
    
    def update(self, request, pk=None):
        try:
            wargame_user = WargameUser.objects.get(pk=pk)
            serializer = WargameUserUpdateSerializer(wargame_user, data=request.data, context={'request': request})
            if serializer.is_valid():
                wargame_user.user.username = serializer.validated_data['username']
                wargame_user.user.email = serializer.validated_data['email']
                wargame_user.user.first_name = serializer.validated_data['first_name']
                wargame_user.user.last_name = serializer.validated_data['last_name']
                wargame_user.bio = serializer.validated_data['bio']
                wargame_user.profile_image_url = serializer.validated_data['profile_image_url']
                wargame_user.save()
                serializer = WargameUserUpdateSerializer(wargame_user, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except WargameUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
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
        fields = ('id', 'bio', 'profile_image_url', 'user', 'gamer_events', 'wargame_username')