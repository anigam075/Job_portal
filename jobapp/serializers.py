from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from datetime import datetime

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = UserProfile
        fields = ['user', 'email', 'dob', 'address', 'resume_link']

    def create(self, validated_data):
        user = validated_data.pop('user')
        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationData
        fields = ['college', 'degree', 'specialization', 'start_date', 'end_date']

    def create(self, validated_data):
        user = self.context['request'].user  # Get the current logged-in user
        email = user.email  # Get the current logged-in user's email
        education_data = EducationData.objects.create(
            user=user,
            email=email,
            is_deleted='0',  # Set is_deleted to '0'
            created_at=datetime.now(),  # Set created_at to the current date
            **validated_data
        )
        return education_data


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = ['job_title', 'company_name', 'start_date', 'end_date', 'description']

    def create(self, validated_data):
        user = self.context['request'].user  # Get the current logged-in user
        email = user.email  # Get the current logged-in user's email
        job_data = WorkExperience.objects.create(
            user=user,
            email=email,
            is_deleted='0',  # Set is_deleted to '0'
            created_at=datetime.now(),  # Set created_at to the current date
            **validated_data
        )
        return job_data