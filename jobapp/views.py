from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import *
from .serializers import *
from django.db.models import Q
import random    
from django.template.response import TemplateResponse

class IndexView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        context = {}
        if request.user.is_authenticated:
            context['username'] = request.user.username
        if 'search' in request.query_params:
            # Job search logic
            query = request.query_params.get('search', None)
            if query:
                queryset = Company.objects.filter(
                    Q(job_title__icontains=query) |
                    Q(company_name__icontains=query) |
                    Q(job_location__icontains=query)
                ).filter(is_deleted=0)
            else:
                queryset = Company.objects.filter(is_deleted=0)
                if queryset.exists():
                    queryset = random.sample(list(queryset), min(len(queryset), 5))
            
            serializer = CompanySerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            # Render the index page
            return render(request, 'index.html', context)

class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout Successful"}, status=status.HTTP_200_OK)

class SignupAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            
            # Extract additional data for the user profile
            profile_data = {
                'user': user.id,
                'email': request.data.get('email'),
                'dob': request.data.get('dob'),
                'address': request.data.get('address'),
                'resume_link': request.data.get('resume_link')
            }
            profile_serializer = UserProfileSerializer(data=profile_data)
            if profile_serializer.is_valid():
                profile_serializer.save()
            else:
                return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Authenticate the user
            user = authenticate(username=request.data.get('email'), password=request.data.get('password'))
            if user is not None:
                login(request, user)  # Using session-based login
                return Response({'user': user_serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)
                
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddEducationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return render(request, 'add_education.html')

    def post(self, request):
        serializer = EducationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddJobAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return render(request, 'add_job_details.html')

    def post(self, request):
        print('POST request made')
        serializer = JobSerializer(data=request.data, context={'request': request})
        print('serializer ============ > ', serializer)
        if serializer.is_valid():
            print('saving serializer')
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return Response({'username': user.username})
        return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Render the login page
        return render(request, 'login.html')

    def post(self, request):
        # Extract email and password from the request
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, username=email, password=password)
        print(user)

        if user is not None:
            # Login the user using session-based authentication
            login(request, user)

            # Return response indicating successful login
            return Response({
                'success': 'Login successful',
                'user_id': user.id,
                'email': user.email
            }, status=status.HTTP_200_OK)
        else:
            # Return error response if authentication fails
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        print('user========= > ', user)
        # Retrieve user profile data
        profile = UserProfile.objects.filter(user=user).first()
        print('user========= > ', profile)
        education = EducationData.objects.filter(user=user, is_deleted=0)
        print('education========= > ', education)
        experience = WorkExperience.objects.filter(user=user, is_deleted=0)
        print('experience========= > ', experience)

        # Serialize data
        profile_serializer = UserProfileSerializer(profile)
        # print('profile_serializer========= > ', profile_serializer)
        education_serializer = EducationSerializer(education, many=True)
        # print('education_serializer========= > ', education_serializer)
        experience_serializer = JobSerializer(experience, many=True)
        # print('experience_serializer========= > ', experience_serializer)

        # Render the template with the user data
        context = {
            'profile': profile_serializer.data,
            'education': education_serializer.data,
            'experience': experience_serializer.data
        }
        print('context ========== > ', context)
        # context = {
        #     'profile': profile_serializer.data,
        #     'education': education_serializer.data,
        #     'experience': experience_serializer.data
        # }
        return TemplateResponse(request, 'user_profile.html', context)

    def post(self, request):
        user = request.user
        # Handle profile update
        profile_data = request.data.get('profile')
        if profile_data:
            profile = UserProfile.objects.filter(user=user).first()
            if profile:
                profile_serializer = UserProfileSerializer(profile, data=profile_data, partial=True)
                if profile_serializer.is_valid():
                    profile_serializer.save()
                else:
                    return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Handle education update
        education_data = request.data.get('education')
        if education_data:
            for item in education_data:
                if 'id' in item:
                    # Update existing education
                    education = EducationData.objects.get(id=item['id'])
                    education_serializer = EducationSerializer(education, data=item, partial=True)
                else:
                    # Create new education
                    education_serializer = EducationSerializer(data=item, context={'request': request})

                if education_serializer.is_valid():
                    education_serializer.save()
                else:
                    return Response(education_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Handle experience update
        experience_data = request.data.get('experience')
        if experience_data:
            for item in experience_data:
                if 'id' in item:
                    # Update existing experience
                    experience = WorkExperience.objects.get(id=item['id'])
                    experience_serializer = JobSerializer(experience, data=item, partial=True)
                else:
                    # Create new experience
                    experience_serializer = JobSerializer(data=item, context={'request': request})

                if experience_serializer.is_valid():
                    experience_serializer.save()
                else:
                    return Response(experience_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Profile, education, and experience updated successfully'}, status=status.HTTP_200_OK)
