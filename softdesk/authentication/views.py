from django.shortcuts import render
from rest_framework.response import Response

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
    
    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().list(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


