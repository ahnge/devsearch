from django.urls import path
from . import views

app_name = 'projects'
urlpatterns = [
    path('', views.ProjectsView.as_view(), name='all_pjs'),
    path('project/<str:pk>', views.ProjectView.as_view(), name='sg_pj'),
    path('create-project/', views.CreateProject.as_view(), name='create_project'),
    path('project/<str:pk>/update-project/',
         views.UpdateProject.as_view(), name='update_project'),
    path('project/<str:pk>/delete-project/',
         views.DeleteProject.as_view(), name='delete_project'),
]
