from django.contrib import admin

from ufo_api.models import Sighting

# make models data available in admin site
admin.site.register(Sighting)
