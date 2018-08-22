from django.shortcuts import render
from rest_framework import generics
from .serializers import FoodSerializer
from .models import Food

# Create your views here.
class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new food."""
        serializer.save()

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT, and DELETE requests."""

    queryset = Food.objects.all()
    serializer_class = FoodSerializer
