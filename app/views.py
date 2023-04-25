from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin

from .serlializers import ItemSerializer
from .models import Item

# Create your views here.
class ApiTest(ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, generics.GenericAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = "id"
    
    def get_object(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise Http404

    def get(self, request,  *args, **kwargs):
        # if pk == None:
        #     print("asdasdasds")
        return self.list(request, *args, **kwargs)
        # item = Item.objects.all()
        # serializer = ItemSerializer(item, many=True)
        # return Response(serializer.data)
    
    def post(self, request):
        item_serializer = ItemSerializer(data=request.data)
        if item_serializer.is_valid():
            item_serializer.save()
            return Response(item_serializer.data, status=status.HTTP_201_CREATED)
        return Response(item_serializer.error, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format = None):
        item_filtered = self.get_object(pk)
        item_serializer = ItemSerializer(item_filtered, data=request.data)
        if item_serializer.is_valid():
            item_serializer.save()
            return Response(item_serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(item_serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item_filtered = self.get_object(pk)
        item_filtered.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


