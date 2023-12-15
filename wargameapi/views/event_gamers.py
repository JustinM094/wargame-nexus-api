from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from wargameapi.models import EventGamer, WargameUser, Army, Event
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response

class WargameUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WargameUser
        fields = ('id', 'wargame_username')

class ArmySerializer(serializers.ModelSerializer):
    class Meta:
        model = Army
        fields = fields = ('id', 'name', 'image_url', 'points', 'description', 'category', 'user',)

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'host', 'event_name', 'event_location', 'event_time', 'game',)

class EventGamerSerializer(serializers.ModelSerializer):
    user = WargameUserSerializer()
    event = EventSerializer()
    army = ArmySerializer()
    class Meta:
        model = EventGamer
        fields = ['id', 'user', 'event', 'timestamp', 'army']

class EventGamerView(ViewSet):

    def list(self, request):
        event_gamers = EventGamer.objects.all()
        serialized = EventGamerSerializer(event_gamers, many=True, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        try:
            single_event_gamer = EventGamer.objects.get(pk=pk)
            serialized = EventGamerSerializer(single_event_gamer, context={'request': request})
            return Response(serialized.data, status=status.HTTP_200_OK)
        except EventGamer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        try:
            event_id = request.data.get('event')
            army_id = request.data.get('army')

            event_gamer = EventGamer.objects.create(
                user=request.user.wargameuser,
                event_id=event_id,
                army_id=army_id,
            )

            serializer = EventGamerSerializer(event_gamer, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def destroy(self, request, pk=None):
        try:
            event = EventGamer.objects.get(pk=pk)
            if request.user.wargameuser.id != event.host_id:
                raise PermissionDenied("You do not have permission to delete this event.")
            event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)