# myapp/management/commands/register_garages.py
import requests
from django.core.management.base import BaseCommand
from api.models import Garage, Address, GarageLocation

class Command(BaseCommand):
    help = 'Find and register petrol garages using Google Places API'

    def add_arguments(self, parser):
        parser.add_argument('latitude', type=float, help='Latitude of the location')
        parser.add_argument('longitude', type=float, help='Longitude of the location')
        parser.add_argument('--radius', type=int, default=5000, help='Search radius in meters')

    def handle(self, *args, **kwargs):
        latitude = kwargs['latitude']
        longitude = kwargs['longitude']
        radius = kwargs['radius']
        api_key = 'AIzaSyDiHrKj-8FFB0_Z8a287zqQLPJiAN8_JXQ'
        endpoint_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

        params = {
            'location': f'{latitude},{longitude}',
            'radius': radius,
            'type': 'gas_station',
            'key': api_key
        }

        try:
            response = requests.get(endpoint_url, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f'HTTP request failed: {e}'))
            return

        results = response.json().get('results', [])

        for result in results:
            name = result.get('name')
            address = result.get('vicinity')
            lat = result['geometry']['location']['lat']
            lng = result['geometry']['location']['lng']

            try:
                # Check if the address already exists, if not create it
                address_instance, created = Address.objects.get_or_create(
                    street_address=address,
                    defaults={
                        'city': '',  # Parse city, state, and zip code if needed
                        'state': '',
                        'zip_code': ''
                    }
                )

                # Check if the garage already exists based on name and address
                garage, created = Garage.objects.update_or_create(
                    name=name,
                    address=address_instance,
                    defaults={
                        'phone_number': '',  # Add phone number if available
                        'email': '',  # Add email if available
                        'refiller_count': 0,
                        'opening_time': None,  # Add opening time if available
                        'closing_time': None  # Add closing time if available
                    }
                )

                # Update or create the garage location
                GarageLocation.objects.update_or_create(
                    garage=garage,
                    defaults={
                        'latitude': lat,
                        'longitude': lng
                    }
                )

                self.stdout.write(self.style.SUCCESS(f'Registered or updated garage: {name}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error registering garage: {e}'))

        self.stdout.write(self.style.SUCCESS('Finished registering garages'))
