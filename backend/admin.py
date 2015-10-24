from django.contrib import admin

# Register your models here.
from .models import Landmark

class LandmarkAdmin(admin.ModelAdmin):
    list_display = ["__unicode__","landmark_id","latitude","longitude","data","duration"]
    class Meta:
        model = Landmark

admin.site.register(Landmark, LandmarkAdmin)