from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from api.models import Food
from api.serializers import FoodSerializer
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

    def create(self, request):
        params = request.data['food']
        if 'name' in params.keys() and 'calories' in params.keys():
            food = Food.objects.create(name=params['name'], calories=params['calories'])
            serializer = FoodSerializer(food)
            return Response(serializer.data)
        else:
            return HttpResponse(status=404)
