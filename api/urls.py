from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.Routes.as_view()),
    path('projects/', views.ProjectsView.as_view()),
    path('projects/<str:pk>/', views.ProjectView.as_view()),
    path('projects/<str:pk>/vote/', views.VoteProjectView.as_view()),

    path('remove-tag/', views.RemoveTagView.as_view())
]
