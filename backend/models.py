from django.db import models

# Create your models here.
class Landmark(models.Model):
    landmark_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)
    data = models.TextField(blank=False)
    duration = models.IntegerField(blank=False,default=10)

    def __unicode__(self):
        return self.name