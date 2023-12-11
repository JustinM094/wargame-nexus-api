from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.core.exceptions import PermissionDenied
from wargameapi.models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'host', 'event_name', 'event_location', 'event_time', 'game',)

class EventUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'host', 'event_name', 'event_location', 'event_time', 'game',)

class EventView(ViewSet):
    def list(self, request):
        event = Event.objects.all()
        serialized = EventSerializer(event, many=True, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        try:
            single_event = Event.objects.get(pk=pk)
            event_serialized = EventSerializer(single_event, context={'request': request})
            return Response(event_serialized.data)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        event_name = request.data.get('event_name')
        event_location = request.data.get('event_location')
        event_time = request.data.get('event_time')
        game_id = request.data.get('game_id')

        event = Event.objects.create(
            host=request.user.wargameuser,
            event_name=event_name,
            event_location=event_location,
            event_time=event_time,
            game_id=game_id,
        )

        serializer = EventSerializer(event, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventUpdateSerializer(event, data=request.data, context={'request': request})
            if serializer.is_valid():
                event.host = serializer.validated_data['host']
                event.event_name = serializer.validated_data['event_name']
                event.event_location = serializer.validated_data['event_location']
                event.event_time = serializer.validated_data['event_time']
                event.game = serializer.validated_data['game']
                event.save()
                serializer = EventUpdateSerializer(event, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        try:
            event = Event.objects.get(pk=pk)
            if request.user.wargameuser.id != event.host_id:
                raise PermissionDenied("You do not have permission to delete this event.")
            event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

