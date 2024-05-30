from django.urls import path
from .views import register, user_login, user_logout


urlpatterns = [
    path('account/register/', register, name='register'),
    path('account/login/', user_login, name='login'),
    path('account/logout/', user_logout, name='logout')
]