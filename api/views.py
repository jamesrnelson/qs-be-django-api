from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from api.models import Food
from api.serializers import FoodSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
import json

class FoodViews(viewsets.ViewSet):
    def list(self, request):
        foods = Food.objects.all()
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data)

    def find(self, request, food_id):
        food = Food.objects.get(pk=food_id)
        serializer = FoodSerializer(food)
        return Response(serializer.data)

    def create(self, request):
        params = request.data['food']
        if 'name' in params.keys() and 'calories' in params.keys():
            food = Food.objects.create(name=params['name'], calories=params['calories'])
            serializer = FoodSerializer(food)
            return Response(serializer.data)
        else:
            return HttpResponse(status=404)

    def update(self, request, food_id):
        params = request.data['food']
        food = Food.objects.get(pk=food_id)
        food.name = params['name']
        food.calories = params['calories']
        food.save()
        serializer = FoodSerializer(food)
        return Response(serializer.data)
