from rest_framework import viewsets, status
from .permissions import IsAuthorOrReadOnly, IsContributor
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist

from .models import Project, Issue, Comment
from authentication.models import Contributor, User
from .serializers import ProjectSerializer, IssueSerializer, CommentSerializer


class ProjectViewset(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        return Project.objects.all()

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        project = self.get_object()
        user = request.user
        serializer = self.get_serializer(project)
        contributor, created = Contributor.objects.get_or_create(
            user=user, project=project
        )
        if contributor in project.contributors.all():
            return Response(
                {"message": "User is already a contributor to this project."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif created:
            contributor.save()
            project.save()
            serializer = self.get_serializer(project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)


class IssueViewset(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthorOrReadOnly, IsContributor]

    def get_queryset(self):
        return Issue.objects.filter(project=self.kwargs["project_pk"])

    @action(detail=True, methods=["post"])
    def add_contributor(self, request, pk=None, project_pk=None):
        issue = self.get_object()
        project = issue.project
        try:
            user = User.objects.get(username=request.data["contributor"])
        except ObjectDoesNotExist:
            return Response(
                {"message": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(issue)
        try:
            contributor = Contributor.objects.get(user=user, project=project)
        except ObjectDoesNotExist:
            return Response(
                {"message": "User is not a contributor to this project."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if contributor.issue == issue:
            return Response(
                {"message": "User is already a contributor to this issue."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            contributor.issue = issue
            contributor.save()
            issue.save()
            serializer = self.get_serializer(issue)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, IsContributor]

    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs["issue_pk"])
