from django.urls import path
from tradeapp.endpoints.register import RegisterView
from tradeapp.endpoints.login import LoginView
from rest_framework_simplejwt.views import TokenRefreshView
from tradeapp.endpoints.resetpassword_view import ResetPasswordView
from tradeapp.endpoints.company_list import CompanyListAPIView
from tradeapp.endpoints.watchlist_view import AddToWatchlistView


urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('api/companies/', CompanyListAPIView.as_view(), name='company-list'),
    path('api/watchlist/add/', AddToWatchlistView.as_view(), name='add-to-watchlist'),
    path('api/watchlist/remove/', AddToWatchlistView.as_view(), name='remove_watchlist'),
    path('api/watchlist/', AddToWatchlistView.as_view(), name='get_user_watchlist'),

]