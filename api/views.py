from django.shortcuts import render
from .serializers import FoodSerializer
from .models import Food
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
import json

# Create your views here.
class FoodViews(viewsets.ViewSet):
    def list(self, request):
        """This method defines the list behavior of the foods api."""
        queryset = Food.objects.all()
        serializer = FoodSerializer(queryset, many=True)
        return Response(serializer.data)

    def find(self, request, food_id):
        """This method defines the find behavior of the foods api."""
        
        queryset = Food.objects.get(pk=food_id)
        serializer = FoodSerializer(queryset)
        return Response(serializer.data)
