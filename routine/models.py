from django.db import models
from django.contrib.auth.models import User
class Routine(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]
    
    TIME_SLOT_CHOICES = [
        ('8-10', '8:00-10:00'),
        ('10-12', '10:00-12:00'),
        ('12-2', '12:00-2:00'),
        ('2-4', '2:00-4:00'),
        ('4-6', '4:00-6:00'),
    ]
    
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    time_slot = models.CharField(max_length=5, choices=TIME_SLOT_CHOICES)
    course_code = models.CharField(max_length=20)
    course_name = models.CharField(max_length=100, blank=True)
    
    class Meta:
        unique_together = ('day', 'time_slot')
        ordering = ['day', 'time_slot']
    
    def __str__(self):
        return f"{self.day} {self.get_time_slot_display()} - {self.course_code}"