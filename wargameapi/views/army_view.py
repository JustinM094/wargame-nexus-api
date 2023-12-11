from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.core.exceptions import PermissionDenied
from wargameapi.models import Army, WargameUser, Category

class ArmySerializer(serializers.ModelSerializer):
    class Meta:
        model = Army
        fields = ('id', 'name', 'image_url', 'points', 'description', 'category', 'user',)

class ArmyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Army
        fields = ('id', 'name', 'image_url', 'points', 'description', 'category', 'user',)

class ArmyView(ViewSet):

    def list(self, request):
        armies = Army.objects.all()
        serialized = ArmySerializer(armies, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        army = Army.objects.get(pk=pk)
        serialized = ArmySerializer(army, many=False)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        name = request.data.get('name')
        image_url = request.data.get('image_url')
        points = request.data.get('points')
        description = request.data.get('description')
        category_id = request.data.get('category')

        army = Army.objects.create(
            user=request.user.wargameuser,
            name=name,
            image_url=image_url,
            points=points,
            description=description,
            category_id=category_id,
        )

        serializer = ArmySerializer(army, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def destroy(self, request, pk=None):
        try:
            army = Army.objects.get(pk=pk)

            if request.user.wargameuser.id != army.user_id:
                raise PermissionDenied("You do not have permission to delete this army.")
            
            army.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Army.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk=None):
        try:
            army = Army.objects.get(pk=pk)
            serializer = ArmyUpdateSerializer(army, data=request.data, context={'request': request})
            if serializer.is_valid():
                army.user = serializer.validated_data['user']
                army.name = serializer.validated_data['name']
                army.image_url = serializer.validated_data['image_url']
                army.points = serializer.validated_data['points']
                army.description = serializer.validated_data['description']
                army.category_id = serializer.validated_data['category']
                army.save()
                serializer = ArmyUpdateSerializer(army, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Army.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)