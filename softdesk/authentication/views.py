from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .models import User, Contributor
from .serializers import UserSerializer, ContributorSerializer
from .permissions import IsCreationOrIsAdmin
from .managers import UserManager
from rest_framework.response import Response

class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes=[IsCreationOrIsAdmin]

    def get_queryset(self):
        return User.objects.all()

