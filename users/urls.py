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

    path('edit-account/', views.EditAccount.as_view(), name='edit_account'),

    path('create-skiill/', views.CreateSkill.as_view(), name="create_skill"),
    path('update-skiill/<str:pk>/',
         views.UpdateSkill.as_view(), name="update_skill"),
    path('delete-skiill/<str:pk>/',
         views.DeleteSkill.as_view(), name="delete_skill"),

    path('inbox/', views.InboxView.as_view(), name="inbox"),
    path('message/<str:pk>/', views.MsgDetailView.as_view(), name="message"),
]
