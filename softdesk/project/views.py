from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import IsAuthorOrStaffOrAdmin
from .models import Project, Issue, Comment
from authentication.models import Contributor
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer
 
class ProjectViewset(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes=[IsAuthorOrStaffOrAdmin, IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        return Project.objects.all()
    
    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().list(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['get'])
    def subscribe(self, request, pk=None):
        project = self.get_object()
        user = request.user
        serializer = self.get_serializer(project)
        contributor, created = Contributor.objects.get_or_create(user=user, project=project)
        if contributor in project.contributors.all():
            return Response({"message": "User is already a contributor to this project."}, status=status.HTTP_400_BAD_REQUEST)
        elif created:
            contributor.save()
            project.save()
            serializer = self.get_serializer(project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)