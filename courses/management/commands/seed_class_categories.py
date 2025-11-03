from django.core.management.base import BaseCommand
from courses.models_class import ClassCategory


class Command(BaseCommand):
    help = "Seed class categories from Nursery to Class 10"

    def handle(self, *args, **kwargs):
        categories = [
            "Nursery",
            "Baby",
            "Class 1",
            "Class 2",
            "Class 3",
            "Class 4",
            "Class 5",
            "Class 6",
            "Class 7",
            "Class 8",
            "Class 9",
            "Class 10",
        ]
        for name in categories:
            ClassCategory.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS("Class categories seeded!"))
