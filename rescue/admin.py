from django.contrib import admin
from .models import AdoptionApplication, Animal, LostFound, RescueReport, VolunteerApplication

admin.site.register([Animal, RescueReport, AdoptionApplication, LostFound, VolunteerApplication])