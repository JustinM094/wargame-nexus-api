from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from wargameapi.models import Army, WargameUser, Category

class ArmySerializer(serializers.ModelSerializer):
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

        

    # def destroy(self, request, pk=None):


