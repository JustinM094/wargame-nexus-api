from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from wargameapi.models import Category 

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)



class CategoryView(ViewSet):
    def list(self, request):
        category = Category.objects.all()
        serialized = CategorySerializer(category, many=True, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)
    def retrieve(self, request, pk=None):
        try:
            single_category = Category.objects.get(pk=pk)
            category_serialized = CategorySerializer(single_category, context={'request': request})
            return Response(category_serialized.data)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)