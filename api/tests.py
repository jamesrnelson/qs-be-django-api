from django.test import TestCase
from api.models import Food
import json
from rest_framework import status
from rest_framework.test import APIClient


class FoodModelTest(TestCase):
    def test_food_saves_to_db(self):
        Food.objects.create(name="hot dog", calories=650)
        weenie = Food.objects.get(name="hot dog")
        count = Food.objects.count()
        self.assertEqual(weenie.name, "hot dog")
        self.assertEqual(weenie.calories, 650)
        self.assertEqual(count, 1)

class FoodEndpointsTest(TestCase):
    def setup(self):
        self.client = APIClient()

    def test_get_all_foods_endpoint_status(self):
        response = self.client.get("/api/v1/foods/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_all_foods_endpoint_json(self):
        food1 = Food.objects.create(name="Banana", calories=150)
        food2 = Food.objects.create(name="Yogurt", calories=550)
        food3 = Food.objects.create(name="Apple", calories=220)

        response = self.client.get("/api/v1/foods/").json()
        self.assertEqual(len(response), 3)
        self.assertEqual(response[0]["name"], food1.name)
        self.assertEqual(response[0]["calories"], food1.calories)
        self.assertEqual(response[1]["name"], food2.name)
        self.assertEqual(response[1]["calories"], food2.calories)

    def test_one_food_endpoint_status(self):
        food1 = Food.objects.create(name="Steak", calories=800)
        food_id = str(food1.id)
        response = self.client.get(f"/api/v1/foods/{food_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_one_food_endpoint_json(self):
        food1 = Food.objects.create(name="Chicken Burrito", calories=1000)
        food_id = str(food1.id)
        response = self.client.get(f"/api/v1/foods/{food_id}").json()
        self.assertEqual(response["name"], food1.name)
        self.assertEqual(response["calories"], food1.calories)

    def test_food_creation_endpoint(self):
        parameters = { "food": { "name": "Pork Kebabs", "calories": 888 } }
        response = self.client.post("/api/v1/foods/", parameters, format="json")
        self.assertEqual(response["name"], parameters["food"]["name"])
        self.assertEqual(response["calories"], parameters["food"]["calories"])
