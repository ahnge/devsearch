from django.urls import path
from .views import projects, project, CreateProject, UpdateProject, DeleteProject

app_name = 'projects'
urlpatterns = [
    path('', projects, name='all_pjs'),
    path('project/<str:pk>', project, name='sg_pj'),
    path('create-project/', CreateProject.as_view(), name='create_project'),
    path('project/<str:pk>/update-project/',
         UpdateProject.as_view(), name='update_project'),
    path('project/<str:pk>/delete-project/',
         DeleteProject.as_view(), name='delete_project'),
]
