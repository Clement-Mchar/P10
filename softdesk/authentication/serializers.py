from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import User, Contributor

class UserSerializer(ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    class Meta:
        model = User
        fields = ['id', 'username', 'password', "birthdate", "can_be_contacted", "can_data_be_shared"]

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            birthdate=validated_data['birthdate'],
            can_be_contacted=validated_data['can_be_contacted'],
            can_data_be_shared=validated_data['can_data_be_shared'],
          )
        user.set_password(validated_data['password']) 
        user.save()
        return user
 
class ContributorSerializer(ModelSerializer):
 
    class Meta:
        model = Contributor
        fields = ['id', 'user', "project"]