from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import FoodViews

urlpatterns = {
    path('foods/', FoodViews.as_view({'get': 'list'})),
    path('foods/<food_id>', FoodViews.as_view({'get': 'find'})),
}

urlpatterns = format_suffix_patterns(urlpatterns)
