from django.contrib import admin
from django.contrib.gis import admin as adminz
from .models import *

# Register your models here.
@admin.register(Images)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("author","name","cover","created_at","updated_at")

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("name","email","subject","message","date")

# subclass the GeoModelAdmin to use the locally hosted OpenLayers library
class olGeoModelAdmin(adminz.GeoModelAdmin):
    openlayers_url = 'OpenLayers.js'

# subclass the OSMGeoAdmin to use the locally hosted OpenLayers library
class olOSMGeoAdmin(adminz.OSMGeoAdmin):
    openlayers_url = 'OpenLayers.js'

@admin.register(Location)
# @admin.register(Location, olOSMGeoAdmin)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name","mpoint")
