from django.shortcuts import render
from .models import Routine

def routine(request):
    # Get all routines ordered by day and time slot
    routines = Routine.objects.all()
    print("sakib")
    print(routines)
    # Structure data for template
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    time_slots = ['8-10', '10-12', '12-2', '2-4', '4-6']
    
    # Create a 2D list for the timetable
    timetable = []
    for day in days:
        day_row = [day]
        for slot in time_slots:
            try:
                routine = routines.get(day=day, time_slot=slot)
                day_row.append({
                    'code': routine.course_code,
                    'name': routine.course_name
                })
            except Routine.DoesNotExist:
                day_row.append(None)
        timetable.append(day_row)
    
    context = {
        'timetable': timetable,
        'time_slots': ['Day'] + time_slots  # Header row
    }
    return render(request, 'courses/routine.html', context)