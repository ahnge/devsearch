import django
from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterUserView.as_view(), name='register'),

    path('', views.Profiles.as_view(), name="all"),
    path('profile/<str:pk>/', views.UserProfile.as_view(), name="user_profile"),
    path('account/', views.UserAccount.as_view(), name="user_account"),

    path('edit-account', views.EditAccount.as_view(), name='edit_account'),
]
