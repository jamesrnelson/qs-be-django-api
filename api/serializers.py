from rest_framework import serializers
from .models import Food, Meal

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('id', 'name', 'calories')

class MealSerializer(serializers.ModelSerializer):
    foods = FoodSerializer(read_only=True, many=True)

    class Meta:
        model = Meal
        fields = ('id', 'name', 'foods')
