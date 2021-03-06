from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import FoodViews, MealViews

urlpatterns = {
    path('foods/', FoodViews.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('foods/<food_id>', FoodViews.as_view({
        'get': 'find',
        'put': 'update',
        'delete': 'destroy',
    })),
    path('meals/', MealViews.as_view({
        'get': 'list',
    })),
    path('meals/<meal_id>/foods', MealViews.as_view({
        'get': 'find',
    })),
    path('meals/<meal_id>/foods/<id>', MealViews.as_view({
        'post': 'add_food',
        'delete': 'destroy_meal_food',
    }))
}

urlpatterns = format_suffix_patterns(urlpatterns)
