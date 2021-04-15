from django.core.management.base import BaseCommand

from persistence.models import Job, CustomUser


class Command(BaseCommand):
    help = 'Invalidates classifier daily cache'

    def handle(self, *args, **options):
        jobs = CustomUser.objects.filter(id__range=(1, 60))
        for job in jobs:
            print(job.id)
