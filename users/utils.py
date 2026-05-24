from .models import Profile, Speciality
from django.db.models import Q # Import the Q object for complex queries

def searchProfiles(request):
    search_query = ''

    if request.GET.get('search_query'): 
        search_query = request.GET.get('search_query')

    speciality = Speciality.objects.filter(name__icontains=search_query) 

    profiles = Profile.objects.distinct().filter( 
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) | 
        Q(speciality__in=speciality)) 


    return profiles, search_query