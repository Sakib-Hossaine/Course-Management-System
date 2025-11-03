from django.db import models
from django.conf import settings

class Note(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    module_code = models.CharField(max_length=20)
    pages = models.IntegerField()
    file = models.FileField(upload_to="notes/")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0)
    download_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Report(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.TextField()
    report_date = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Report on {self.note.title}"
