from django.db import models

# Create your models here.

class Session(models.Model):
    DAY_OF_THE_WEEK = (
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    )
    day_of_the_week = models.CharField(max_length=3, choices=DAY_OF_THE_WEEK)
    time_start_hr = models.IntegerField()
    time_start_min = models.IntegerField()
    time_end_hr = models.IntegerField()
    time_end_min = models.IntegerField()
    room = models.CharField(max_length=50)
    
