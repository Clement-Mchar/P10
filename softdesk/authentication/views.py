from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from .permissions import IsCreationOrIsAdmin, IsUser


class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsCreationOrIsAdmin, IsUser]

    def get_queryset(self):
        return User.objects.all()
