from django.db import models
from math import radians, sin, cos, sqrt, atan2

class Address(models.Model):
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state} {self.zip_code}"

class PredefinedFuel(models.Model):
    fuel_type = models.CharField(max_length=50)
    default_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.fuel_type} - {self.default_price}"

class Fuel(models.Model):
    garage = models.ForeignKey('Garage', on_delete=models.CASCADE, related_name='fuels')
    fuel_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.fuel_type} - {self.price}"

class GarageLocation(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    garage = models.OneToOneField('Garage', on_delete=models.CASCADE, related_name='location')

    def __str__(self):
        return f"Lat: {self.latitude}, Long: {self.longitude}"

    def distance_to(self, other_latitude, other_longitude):
        # Calculate distance using the Haversine formula
        R = 6371  # Radius of the Earth in km

        lat1 = radians(self.latitude)
        lon1 = radians(self.longitude)
        lat2 = radians(other_latitude)
        lon2 = radians(other_longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c  # Distance in km
        return distance


class Facilities(models.Model):
    garage = models.OneToOneField('Garage', on_delete=models.CASCADE, related_name='facilities')
    has_car_wash = models.BooleanField(default=False)
    has_restaurant = models.BooleanField(default=False)
    has_toilet = models.BooleanField(default=False)
    has_atm = models.BooleanField(default=False)

    def __str__(self):
        return f"Facilities for {self.garage.name}"

class Garage(models.Model):
    name = models.CharField(max_length=100)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='garage')
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    refiller_count = models.IntegerField(default=0)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.name
