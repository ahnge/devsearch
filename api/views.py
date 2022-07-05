from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from projects.models import Project, Review, Tag
from django.shortcuts import get_object_or_404, redirect
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
        print(req.user)
        p = Project.objects.all()
        s_projects = ProjectSerializer(p, many=True)
        return Response(s_projects.data)


class ProjectView(APIView):
    def get(self, req, pk):
        pj = Project.objects.get(id=pk)
        s_project = ProjectSerializer(pj, many=False)
        return Response(s_project.data)


class VoteProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, req, pk):
        user = req.user.profile
        pj = Project.objects.get(id=pk)
        data = req.data

        review, created = Review.objects.get_or_create(
            owner=user,
            project=pj
        )
        review.value = data['value']
        review.save()
        pj.getVoteCount

        s_pj = ProjectSerializer(pj, many=False)
        return Response(s_pj.data)


class RemoveTagView(APIView):

    def delete(self, req):
        pk = req.data['id']
        tag = get_object_or_404(Tag, id=pk)
        tag.delete()
        return Response("tag was deleted")
