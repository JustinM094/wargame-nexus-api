from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from wargameapi.models import System

class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = ('id', 'name')

class SystemView(ViewSet):
    def list(self, request):
        system = System.objects.all()
        serialized = SystemSerializer(system, many=True, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)
    def retrieve(self, request, pk=None):
        try:
            single_system = System.objects.get(pk=pk)
            system_serialized = SystemSerializer(single_system, context={'request': request})
            return Response(system_serialized.data)
        except System.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)