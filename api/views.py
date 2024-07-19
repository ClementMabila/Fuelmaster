from django.shortcuts import render
from .models import GarageLocation, Garage
from django.http import JsonResponse

def home(request):
    user_latitude = request.session.get('latitude')
    user_longitude = request.session.get('longitude')

    if user_latitude and user_longitude:
        garages = Garage.objects.all()
        nearby_garages = []

        for garage in garages:
            location = garage.location
            distance = location.distance_to(float(user_latitude), float(user_longitude))
            nearby_garages.append((garage, distance))

        # Sort garages by distance
        nearby_garages.sort(key=lambda x: x[1])
    else:
        nearby_garages = []

    context = {
        'nearby_garages': nearby_garages
    }
    return render(request, 'home.html', context)

def update_location(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Store the location in the session or wherever you need
        request.session['latitude'] = latitude
        request.session['longitude'] = longitude

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})