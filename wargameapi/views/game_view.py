from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.core.exceptions import PermissionDenied
from wargameapi.models import Game, System

class GameUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'game_name', 'image_url', 'description', 'points', 'max_players', 'system_id', 'creator_id',)


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ('id', 'game_name', 'image_url', 'description', 'points', 'max_players', 'system_id', 'creator_id',)

class GameView(ViewSet):
    def list(self, request):
        game = Game.objects.all()
        serialized = GameSerializer(game, many=True, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        try:
            single_game = Game.objects.get(pk=pk)
            game_serialized = GameSerializer(single_game, context={'request': request})
            return Response(game_serialized.data)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        game_name = request.data.get('game_name')
        image_url = request.data.get('image_url')
        description = request.data.get('description')
        points = request.data.get('points')
        max_players = request.data.get('max_players')
        system_id = request.data.get('system_id')

        if not game_name:
            return Response({'error': 'Game name is required.'}, status=status.HTTP_400_BAD_REQUEST)


        system = System.objects.get(pk=system_id)

        game = Game.objects.create(
            game_name=game_name,
            image_url=image_url,
            description=description,
            points=points,
            max_players=max_players,
            system=system,
            creator=request.user.wargameuser,
        )
        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameUpdateSerializer(game, data=request.data, context={'request': request})
            if serializer.is_valid():
                game.creator = serializer.validated_data['creator']
                game.game_name = serializer.validated_data['game_name']
                game.image_url = serializer.validated_data['image_url']
                game.description = serializer.validated_data['description']
                game.points = serializer.validated_data['points']
                game.max_players = serializer.validated_data['max_players']
                game.system= serializer.validated_data['system']
                game.save()
                serializer = GameUpdateSerializer(game, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        try:
            game = Game.objects.get(pk=pk)
            if request.user.wargameuser.id != game.creator_id:
                raise PermissionDenied("You do not have permission to delete this game.")
            game.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)