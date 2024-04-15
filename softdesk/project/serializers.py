from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from authentication.models import Contributor, User
 
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
            project.save()
            contributor.save()
            
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
    contributors = serializers.SerializerMethodField()
    class Meta:
        model = Issue
        fields = ['id', "title", "description", "priority", "tag", 'status', "contributors", "time_created"]
    def get_contributors(self, obj):
        contributors = obj.contributors.all()
        return [contributor.username for contributor in contributors]
    
    def create(self, validated_data):
        project_id = self.context['view'].kwargs.get('project_pk')
        project = Project.objects.get(id=project_id)
        issue = Issue.objects.create(author=self.context['request'].user, project=project, **validated_data)
        contributor = Contributor.objects.get(user=issue.author, project=project)
        contributor.issue=issue
        issue.save()
        contributor.save()

        return issue

class CommentSerializer(ModelSerializer):
 
    class Meta:
        model = Comment
        fields = ['id', 'issue', "comment", "author", "time_created"]