from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from api.models import Food, Meal
from api.serializers import FoodSerializer, MealSerializer
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
        food = get_object_or_404(Food, pk=food_id)
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
        if 'name' in params.keys() and 'calories' in params.keys():
            food = get_object_or_404(Food, pk=food_id)
            food.name = params['name']
            food.calories = params['calories']
            food.save()
            serializer = FoodSerializer(food)
            return Response(serializer.data)
        else:
            return HttpResponse(status=400)

    def destroy(self, request, food_id):
        food = get_object_or_404(Food, pk=food_id)
        import pdb; pdb.set_trace()
        if len(food.meals.all()) > 0:
            return HttpResponse(status=304)
        else:
            food.delete()
            return HttpResponse(status=204)

class MealViews(viewsets.ViewSet):
    def list(self, request):
        meals = Meal.objects.all()
        serializer = MealSerializer(meals, many=True)
        return Response(serializer.data)

    def find(self, request, meal_id):
        meal = get_object_or_404(Meal, pk=meal_id)
        serializer = MealSerializer(meal)
        return Response(serializer.data)

    def add_food(self, request, meal_id, id):
        meal = get_object_or_404(Meal, pk=meal_id)
        food = get_object_or_404(Food, pk=id)
        meal_name = str(meal.name)
        food_name = str(food.name)
        meal.foods.add(food)
        message = {"message": f"Successfully added {food_name} to {meal_name}"}
        return HttpResponse(json.dumps(message), content_type='application/json', status=201)

    def destroy_meal_food(self, request, meal_id, id):
        meal = get_object_or_404(Meal, pk=meal_id)
        food = get_object_or_404(Food, pk=id)
        meal.foods.remove(food)
        meal_name = str(meal.name)
        food_name = str(food.name)
        message = {"message": f"Successfully removed {food_name} from {meal_name}"}
        return HttpResponse(json.dumps(message), content_type='application/json')
