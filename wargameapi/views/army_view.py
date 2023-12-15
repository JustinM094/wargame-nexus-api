from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.core.exceptions import PermissionDenied
from wargameapi.models import Army, WargameUser, Category

class WargameUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WargameUser
        fields = ('id', 'wargame_username')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class CategoryUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class ArmySerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    user = WargameUserSerializer()

    is_owner = serializers.SerializerMethodField()
    def get_is_owner(self, obj):
    # Check if the authenticated user is the owner
        return self.context['request'].user.id == obj.user_id

    class Meta:
        model = Army
        fields = ('id', 'name', 'image_url', 'points', 'description', 'category', 'user', 'is_owner',)

class ArmyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Army
        fields = ('name', 'image_url', 'points', 'description', 'category',)

        extra_kwargs = {"category": {"required": False}}

class ArmyView(ViewSet):

    def list(self, request):
        armies = Army.objects.all()
        serialized = ArmySerializer(armies, many=True, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            single_army = Army.objects.get(pk=pk)
            serialized = ArmySerializer(single_army, context={'request': request})
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Army.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        try:
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
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



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
        # test = 1
        try:
            army = Army.objects.get(pk=pk)
            serializer = ArmyUpdateSerializer(army, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                # army.user = WargameUser.objects.get(user=request.auth.user)
                army.name = serializer.validated_data['name']
                army.image_url = serializer.validated_data['image_url']
                army.points = serializer.validated_data['points']
                army.description = serializer.validated_data['description']
                army.category = serializer.validated_data['category']
                army.save()
                serializer = ArmyUpdateSerializer(army, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Army.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)