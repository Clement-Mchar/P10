from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from authentication.models import Contributor, User
from django.urls import reverse
from .models import Project, Issue, Comment


class ProjectSerializer(ModelSerializer):
    author = serializers.SerializerMethodField()
    contributors = serializers.SerializerMethodField()
    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "contributors",
            "type",
            "author",
            "time_created",
            "issues",
        ]

    def create(self, validated_data):
        if self.context["request"].user.is_authenticated:
            project = Project.objects.create(
                name=validated_data["name"],
                description=validated_data["description"],
                type=validated_data["type"],
                author=self.context["request"].user,
            )
            contributor = Contributor.objects.create(
                user=self.context["request"].user, project=project
            )
            project.save()
            contributor.save()

            return project
        else:
            return None

    def get_author(self, obj):
        return obj.author.username

    def get_contributors(self, obj):
        user = self.context["request"].user
        contributors = obj.contributors.all()
        if user in contributors:
            return [contributor.username for contributor in contributors]

    def get_issues(self, obj, *args, **kwargs):
        user = self.context["request"].user
        if user in obj.contributors.all():
            return [issue.title for issue in obj.issue_set.all()]
        else:
            return kwargs.pop("issues", None)


class IssueSerializer(ModelSerializer):
    contributors = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "priority",
            "tag",
            "status",
            "contributors",
            "comments",
            "time_created",
        ]

    def get_contributors(self, obj):
        contributors = obj.contributors.all()
        return [contributor.username for contributor in contributors]

    def create(self, validated_data):
        project_id = self.context["view"].kwargs.get("project_pk")
        project = Project.objects.get(id=project_id)
        issue = Issue.objects.create(
            author=self.context["request"].user, project=project, **validated_data
        )
        if self.context["request"].user in project.contributors.all():

            contributor = Contributor.objects.get(user=issue.author, project=project)
            contributor.issue = issue
            issue.save()
            contributor.save()

        return issue

    def get_comments(self, obj):
        return [comment.comment for comment in obj.comment_set.all()]


class CommentSerializer(ModelSerializer):

    issue_url = serializers.SerializerMethodField()

    author = serializers.SerializerMethodField()
    issue = serializers.SerializerMethodField()

    def create(self, validated_data):
        issue_id = self.context["view"].kwargs.get("issue_pk")
        issue = Issue.objects.get(id=issue_id)
        comment = Comment.objects.create(
            issue=issue, author=self.context["request"].user, **validated_data
        )
        comment.save()
        return comment

    def get_author(self, obj):
        return obj.author.username

    def get_issue(self, obj, *args, **kwargs):
        issue_id = self.context["view"].kwargs.get("issue_pk")
        issue = Issue.objects.get(id=issue_id)
        return issue.title

    def get_issue_url(self, obj):
        issue = obj.issue
        if issue:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(
                    reverse(
                        "project-issues-detail",
                        kwargs={"project_pk": issue.project.id, "pk": issue.id},
                    )
                )
        return None

    class Meta:
        model = Comment
        fields = ["id", "issue_url", "issue", "comment", "author", "time_created"]
