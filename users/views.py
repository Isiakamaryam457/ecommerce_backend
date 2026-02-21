from django.shortcuts import render
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

# Register a new user
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] # anyone can register

# Get, Update, Delete a user
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated] # must be logged in





