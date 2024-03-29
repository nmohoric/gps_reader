from django.db import models

class Activity(models.Model):
    activity = models.CharField(max_length=200)
    sport = models.CharField(max_length=100)
    time_s = models.FloatField('time in seconds')
    distance_m = models.FloatField('distance in meters')
    date = models.DateTimeField('start date/time')

    def __unicode__(self):
        return self.activity
