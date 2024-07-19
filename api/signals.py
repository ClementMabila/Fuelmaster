from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models import *

@receiver(post_save, sender=Garage)
def create_fuel_types(sender, instance, created, **kwargs):
    if created:
        predefined_fuels = PredefinedFuel.objects.all()
        for fuel in predefined_fuels:
            Fuel.objects.create(garage=instance, fuel_type=fuel.fuel_type, price=fuel.default_price)
