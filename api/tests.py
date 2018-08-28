import json
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from api.models import Food, Meal


class FoodModelTest(TestCase):
    def test_food_saves_to_db(self):
        Food.objects.create(name='hot dog', calories=650)
        food1 = Food.objects.get(name='hot dog')
        count = Food.objects.count()
        self.assertEqual(food1.name, 'hot dog')
        self.assertEqual(food1.calories, 650)
        self.assertEqual(count, 1)

class MealModelTest(TestCase):
    def test_meal_saves_to_db(self):
        Meal.objects.create(name='Breakfast')
        meal1 = Meal.objects.get(name='Breakfast')
        food1 = Food.objects.create(name='Huevos Rancheros', calories=555)
        food2 = Food.objects.create(name='Bacon', calories=777)
        food3 = Food.objects.create(name='Smoked Salmon Scramble', calories=600)
        meal1.foods.add(food1, food2, food3)

        meal_count = Meal.objects.count()
        foods_count = meal1.foods.count()
        self.assertEqual(meal1.name, 'Breakfast')
        self.assertEqual(meal_count, 1)
        self.assertEqual(foods_count, 3)

class FoodEndpointsTest(TestCase):
    def setup(self):
        self.client = APIClient()

    def test_get_all_foods_endpoint_status(self):
        response = self.client.get('/api/v1/foods/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_all_foods_endpoint_json(self):
        food1 = Food.objects.create(name='Banana', calories=150)
        food2 = Food.objects.create(name='Yogurt', calories=550)
        food3 = Food.objects.create(name='Apple', calories=220)

        response = self.client.get('/api/v1/foods/').json()
        self.assertEqual(len(response), 3)
        self.assertEqual(response[0]['name'], food1.name)
        self.assertEqual(response[0]['calories'], food1.calories)
        self.assertEqual(response[1]['name'], food2.name)
        self.assertEqual(response[1]['calories'], food2.calories)

    def test_one_food_endpoint_status(self):
        food1 = Food.objects.create(name='Steak', calories=800)
        food_id = str(food1.id)
        response = self.client.get(f'/api/v1/foods/{food_id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_one_food_endpoint_json(self):
        food1 = Food.objects.create(name='Chicken Burrito', calories=1000)
        food_id = str(food1.id)
        response = self.client.get(f'/api/v1/foods/{food_id}').json()
        self.assertEqual(response['name'], food1.name)
        self.assertEqual(response['calories'], food1.calories)

    def test_food_creation_endpoint(self):
        response = self.client.post('/api/v1/foods/', json.dumps({'food': {'name': 'Pork Kebabs', 'calories': 800}}), content_type='application/json')
        food_response = response.json()

        self.assertEqual(food_response['name'], 'Pork Kebabs')
        self.assertEqual(food_response['calories'], 800)

    def test_food_creation_error_handling(self):
        response = self.client.post(
            '/api/v1/foods/',
            json.dumps({'food': {'calories': 800}}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_food_editing_endpoint(self):
        food1 = Food.objects.create(name='Chicken Kiev', calories=555)
        food_id = str(food1.id)
        response = self.client.put(
            f'/api/v1/foods/{food_id}',
            json.dumps({'food': {'name': 'Beef Wellington', 'calories': 777}}),
            content_type='application/json'
        )
        food_response = response.json()

        self.assertEqual(food_response['id'], food1.id)
        self.assertEqual(food_response['name'], 'Beef Wellington')
        self.assertEqual(food_response['calories'], 777)

    def test_food_editing_error_handling(self):
        food1 = Food.objects.create(name='Pasta Naples', calories=555)
        food_id = str(food1.id)
        response = self.client.put(
            f'/api/v1/foods/{food_id}',
            json.dumps({'food': {'name': 'Meatballs Stockholm'}}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_food_deletion_endpoint(self):
        food1 = Food.objects.create(name='Beef Stroganoff', calories=999)
        food_id = str(food1.id)
        response = self.client.delete(f'/api/v1/foods/{food_id}')
        assert response.status_code == 204

        response2 = self.client.get(f'/api/v1/foods/{food_id}')
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

class MealEndpointsTest(TestCase):
    def setup(self):
        self.client = APIClient()

    def test_get_all_meals_endpoint_status(self):
        response = self.client.get('/api/v1/meals/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_meals_endpoint_json(self):
        meal1 = Meal.objects.create(name='Brunch')
        meal2 = Meal.objects.create(name='Lunch')
        food1 = Food.objects.create(name='Huevos Rancheros', calories=555)
        food2 = Food.objects.create(name='Bacon', calories=777)
        food3 = Food.objects.create(name='Smoked Salmon Scramble', calories=600)
        meal1.foods.add(food1, food2, food3)
        meal2.foods.add(food1, food2)


        response = self.client.get('/api/v1/meals/')
        meals_response = response.json()

        self.assertEqual(len(meals_response), 2)
        self.assertEqual(meals_response[0]['name'], meal1.name)
        self.assertEqual(len(meals_response[0]['foods']), 3)
        self.assertEqual(meals_response[0]['foods'][0]['name'], 'Huevos Rancheros')

        self.assertEqual(meals_response[1]['name'], meal2.name)
        self.assertEqual(len(meals_response[1]['foods']), 2)
        self.assertEqual(meals_response[1]['foods'][1]['name'], food2.name)

    def test_find_one_meal(self):
        meal1 = Meal.objects.create(name='Brunch')
        meal2 = Meal.objects.create(name='Lunch')
        food1 = Food.objects.create(name='Huevos Rancheros', calories=555)
        food2 = Food.objects.create(name='Bacon', calories=777)
        food3 = Food.objects.create(name='Smoked Salmon Scramble', calories=600)
        meal1.foods.add(food1, food2, food3)
        meal2.foods.add(food1, food2)

        meal_id = str(meal1.id)
        response = self.client.get(f'/api/v1/meals/{meal_id}/foods')
        meal_response = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(meal_response['name'], meal1.name)
        self.assertEqual(len(meal_response['foods']), 3)
        self.assertEqual(meal_response['foods'][2]['name'], food3.name)

    def test_find_one_meal_error_handling(self):
        meal1 = Meal.objects.create(name='Brunch')
        meal2 = Meal.objects.create(name='Lunch')
        food1 = Food.objects.create(name='Huevos Rancheros', calories=555)
        food2 = Food.objects.create(name='Bacon', calories=777)
        food3 = Food.objects.create(name='Smoked Salmon Scramble', calories=600)
        meal1.foods.add(food1, food2, food3)
        meal2.foods.add(food1, food2)

        response = self.client.get(f'/api/v1/meals/1000000/foods')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
