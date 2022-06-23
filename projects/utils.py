from .models import Project, Tag
from django.db.models import Q


def search_projects(req):
    projects = Project.objects.all()
    ctx = {'projects': projects}

    if req.GET.get('search_query'):
        search_query = req.GET.get('search_query')
        tags = Tag.objects.filter(name__icontains=search_query)
        projects = Project.objects.distinct().filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(owner__name__icontains=search_query) |
            Q(tags__in=tags)
        )
        ctx = {'projects': projects, 'search_query': search_query}

    return ctx
