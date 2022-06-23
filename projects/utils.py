from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def search_projects(req):
    projects = Project.objects.all()
    search_query = ''

    if req.GET.get('search_query'):
        search_query = req.GET.get('search_query')
        tags = Tag.objects.filter(name__icontains=search_query)
        projects = Project.objects.distinct().filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(owner__name__icontains=search_query) |
            Q(tags__in=tags)
        )

    return projects, search_query


def paginate_projects(req, projects):
    page = req.GET.get('page')
    results = 3
    p = Paginator(projects, results)
    try:
        projects = p.page(page)
    except PageNotAnInteger:
        page = 1
        projects = p.page(page)
    except EmptyPage:
        page = p.num_pages
        projects = p.page(page)

    leftIndex = int(page) - 2
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = int(page) + 3
    if rightIndex > p.num_pages:
        rightIndex = p.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, projects
