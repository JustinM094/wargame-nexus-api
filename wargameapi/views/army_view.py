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
    
    # def create(self, request):


    # def destroy(self, request, pk=None):


