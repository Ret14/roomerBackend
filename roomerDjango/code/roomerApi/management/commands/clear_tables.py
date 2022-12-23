from django.core.management import BaseCommand

from roomerApi import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        models.Profile.objects.all().delete()
        models.Interest.objects.all().delete()
        models.Review.objects.all().delete()
        models.Housing.objects.all().delete()
        models.RoomAttribute.objects.all().delete()