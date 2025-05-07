from django.shortcuts import render

# Create your views here.

# testing
from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

#end testing

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView
from .models import MealPlan, FoodItem, UserPreferences
from .serializers import *

# 1. Register API - using dj-rest-auth
class CustomRegisterView(RegisterView):
    pass

# 2. Login API - using dj-rest-auth
class CustomLoginView(LoginView):
    pass

# 3. Logout API - using dj-rest-auth
class CustomLogoutView(LogoutView):
    pass

# 4. Analyze Image API
class AnalyzeImageView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        image = request.FILES.get("image")
        # Dummy response for now
        return Response({
            "foodItems": [
                {"name": "Pizza", "estimatedCalories": 300, "confidence": 0.92},
                {"name": "Salad", "estimatedCalories": 120, "confidence": 0.85}
            ],
            "summary": "Meal includes pizza and salad. Total estimated calories: 420 kcal."
        })

# 5. Search Food Nutrition
@api_view(['GET'])
def search_food_nutrition(request):
    query = request.GET.get('query')
    return Response({
        "results": [{
            "foodId": "123",
            "name": "Apple, raw",
            "nutrients": {"calories": 95, "protein": 0.5, "fat": 0.3, "carbohydrates": 25}
        }]
    })

# 6. Generate Meal Plan
class GenerateMealPlanView(APIView):
    def post(self, request):
        return Response({
            "mealPlan": {
                "Monday": [
                    {"meal": "Breakfast", "items": ["Oatmeal with banana"], "calories": 350},
                ]
            }
        })

# 7. Grocery List
class GetGroceryListView(APIView):
    def post(self, request):
        return Response({
            "groceryList": [
                {"item": "Oats", "quantity": "500g"},
                {"item": "Bananas", "quantity": "6 pcs"}
            ]
        })

# 8. User Preferences
class UserPreferencesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "caloriesPerDay": 2000,
            "dietType": "vegetarian",
            "allergies": ["gluten"]
        })

    def post(self, request):
        return Response({"message": "Preferences updated successfully."})

# 9. Meal Plan History
class MealPlanHistoryView(APIView):
    def get(self, request):
        return Response({
            "history": [
                {"mealPlanId": "mp_001", "dateRange": "2025-05-01 to 2025-05-07"},
                {"mealPlanId": "mp_002", "dateRange": "2025-05-08 to 2025-05-14"}
            ]
        })

# 10. Nutrition Summary
class NutritionSummaryView(APIView):
    def post(self, request):
        return Response({
            "totalCalories": 14000,
            "averagePerDay": 2000,
            "macros": {"protein": "20%", "fat": "30%", "carbs": "50%"}
        })