from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from authentication.models import Contributor
 
from .models import Project, Issue, Comment

class ProjectSerializer(ModelSerializer):
    author= serializers.SerializerMethodField()
    contributors = serializers.SerializerMethodField()
    issues = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = ['id', 'name', "description", "contributors", "type", "author", "time_created", "issues", ]

    def create(self, validated_data):
        if self.context['request'].user.is_authenticated:
            project = Project.objects.create(
                name=validated_data['name'],
                description=validated_data['description'],
                type=validated_data['type'],
                author=self.context['request'].user
              )
            contributor = Contributor.objects.create(
                user=self.context['request'].user,
                project=project
            )
            contributor.save()
            project.save()
            return project
        else:
            return None
    
    def get_author(self, obj):
        return obj.author.username

    def get_contributors(self, obj):
        contributors = obj.contributors.all()
        return [contributor.username for contributor in contributors]
    
    def get_issues(self, obj, *args, **kwargs):
        user = self.context['request'].user
        if user in obj.contributors.all():
            return [issue.title for issue in obj.issue_set.all()]
        else:
            return kwargs.pop('issues', None)

class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', "title", "description", "priority", "tag", "time_created"]

    def create(self, validated_data):
        issue = Issue.objects.create(**validated_data)
        return issue

class CommentSerializer(ModelSerializer):
 
    class Meta:
        model = Comment
        fields = ['id', 'issue', "comment", "author", "time_created"]