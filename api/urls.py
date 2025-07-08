from django.urls import path
from .views import PredictDigitView, PredictionHistoryView, UserProfileView, LoginView, RegisterView

urlpatterns = [
    path('predict/', PredictDigitView.as_view(), name='predict-digit'),
    path('history/', PredictionHistoryView.as_view(), name='prediction-history'),
    path('history/<int:pk>/', PredictionHistoryView.as_view(), name='prediction-detail'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
]