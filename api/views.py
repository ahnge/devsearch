from rest_framework.views import APIView
from rest_framework.response import Response
from projects.models import Project
from .serializers import ProjectSerializer


class Routes(APIView):
    def get(self, req):
        routes = [
            {'GET': '/api/projects'},
            {'GET': '/api/projects/id'},
            {'POST': '/api/projects/id/vote'},

            {'POST': '/api/users/token'},
            {'POST': '/api/users/token/refresh'},
        ]
        return Response(routes)


class ProjectsView(APIView):
    def get(self, req):
        p = Project.objects.all()
        s_projects = ProjectSerializer(p, many=True)
        return Response(s_projects.data)


class ProjectView(APIView):
    def get(self, req, pk):
        pj = Project.objects.get(id=pk)
        s_project = ProjectSerializer(pj, many=False)
        return Response(s_project.data)
