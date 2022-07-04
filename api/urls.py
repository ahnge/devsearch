from django.urls import path
from . import views

urlpatterns = [
    path('', views.Routes.as_view()),
    path('projects/', views.ProjectsView.as_view()),
    path('projects/<str:pk>/', views.ProjectView.as_view()),
]
