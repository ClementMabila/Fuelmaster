from django.contrib import admin
from api.models import Address, PredefinedFuel, Fuel, GarageLocation, Facilities, Garage

admin.site.register(Address)
admin.site.register(PredefinedFuel)
admin.site.register(Fuel)
admin.site.register(GarageLocation)
admin.site.register(Facilities)
admin.site.register(Garage)