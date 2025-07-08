
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from PIL import Image
from django.shortcuts import get_object_or_404
import os

from core.models import PredictionHistory
from core.ml_model import predict_digit
from .serializers import PredictionHistorySerializer, UserSerializer, LoginSerializer

class PredictDigitView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    
    def post(self, request, format=None):
        if 'image' not in request.FILES:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            uploaded_image = request.FILES['image']
            image = Image.open(uploaded_image)
            result = predict_digit(image)
            
            prediction = PredictionHistory.objects.create(
                user=request.user,
                image=uploaded_image,
                result=result
            )
            
            serializer = PredictionHistorySerializer(prediction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PredictionHistoryView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    
    def get(self, request, pk=None, format=None):
        if pk is not None:
            # Single prediction detail
            prediction = get_object_or_404(PredictionHistory, pk=pk, user=request.user)
            serializer = PredictionHistorySerializer(prediction)
            return Response(serializer.data)
        else:
            # All predictions list
            predictions = PredictionHistory.objects.filter(user=request.user)
            serializer = PredictionHistorySerializer(predictions, many=True)
            return Response(serializer.data)
    
    def delete(self, request, pk=None, format=None):
        try:
            prediction = get_object_or_404(PredictionHistory, pk=pk, user=request.user)
            
            # Delete associated file from filesystem
            if prediction.image:
                if os.path.isfile(prediction.image.path):
                    os.remove(prediction.image.path)
            
            prediction.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class UserProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(username=serializer.validated_data['username']).exists():
                return Response(
                    {'username': 'This username already exists.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
                email=serializer.validated_data.get('email', '')
            )
            
            token = Token.objects.create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)