from .models import Skill, Profile
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.tokens import PasswordResetTokenGenerator


def search_profiles(req):
    profiles = Profile.objects.all()
    search_query = ''

    if req.GET.get('search_query'):
        search_query = req.GET.get('search_query')
        skills = Skill.objects.filter(name__icontains=search_query)
        profiles = Profile.objects.distinct().filter(
            Q(name__icontains=search_query) |
            Q(short_intro__icontains=search_query) |
            Q(skill__in=skills)
        )
    return profiles, search_query


def paginate_profiles(req, profiles):
    page = req.GET.get('page')
    results = 3
    p = Paginator(profiles, results)
    try:
        profiles = p.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = p.page(page)
    except EmptyPage:
        page = p.num_pages
        profiles = p.page(page)

    leftIndex = int(page) - 2
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = int(page) + 3
    if rightIndex > p.num_pages:
        rightIndex = p.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, profiles


account_activation_token = PasswordResetTokenGenerator()
