from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import IsAuthorOrStaffOrAdmin
from .models import Project, Issue, Comment
from authentication.models import Contributor
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer
 
class ProjectViewset(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    def get_queryset(self):
        return Project.objects.all()

    @action(detail=True, methods=['post'])
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

class IssueViewset(viewsets.ModelViewSet):
    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs['project_pk'])
    
    def create(self, request,  project_pk=None):
        id = project_pk
        project = Project.objects.get(id=id)
        user = request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            issue = Issue.objects.create(
                project=project,
                author=user,
                **validated_data
            )
            serializer = self.get_serializer(issue)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)