from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
 
from .models import User
from .serializers import UserSerializer
 
class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    def get_queryset(self):
        
        return User.objects.all()