from time import sleep

from django.core.management.base import BaseCommand

from tracker.models import Session, Event


class Command(BaseCommand):
    help = 'Start time tracking'

    def handle(self, *args, **options):
        session, created = Session.objects.get_or_create()
        Event.objects.create(session=session)

        sleep(3)
        Event.objects.create(session=session, working=False)

