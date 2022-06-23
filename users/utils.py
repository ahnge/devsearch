from .models import Skill, Profile
from django.db.models import Q


def search_profiles(req):
    profiles = Profile.objects.all()
    ctx = {'profiles': profiles}

    if req.GET.get('search_query'):
        search_query = req.GET.get('search_query')
        skills = Skill.objects.filter(name__icontains=search_query)
        profiles = Profile.objects.distinct().filter(
            Q(name__icontains=search_query) |
            Q(short_intro__icontains=search_query) |
            Q(skill__in=skills)
        )
        ctx = {'profiles': profiles, 'search_query': search_query}

    return ctx
