import datetime

from django.db import models
from django.utils import timezone


class Session(models.Model):
    day = models.DateField(default=timezone.now)
    duration = models.TimeField(default=datetime.time)
    error = models.BooleanField(default=False)

    def calculate_duration(self):
        start_time = None
        duration = 0
        self.error = False
        events = self.events.all().order_by('timestamp')
        for count, event in enumerate(events):
            if count % 2 == 0 and not event.working or count % 2 == 1 and event.working:
                self.error = True

            if not start_time:
                if event.working:
                    start_time = event.timestamp
            elif start_time:
                if not event.working:
                    if event.is_lunch_time() or event == events.last():
                        duration += (event.timestamp - start_time).total_seconds()
                        start_time = None
        self.duration = datetime.datetime.fromtimestamp(int(duration), timezone.utc).time()
        self.save()

    def __str__(self):
        return str(self.duration)


class Event(models.Model):
    session = models.ForeignKey(Session, models.CASCADE, related_name='events')
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    working = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.session.calculate_duration()

    def is_lunch_time(self):
        start_range = datetime.datetime(self.timestamp.year,
                                        self.timestamp.month,
                                        self.timestamp.day,
                                        11, 30, 0, 0, tzinfo=self.timestamp.tzinfo)
        end_range = datetime.datetime(self.timestamp.year,
                                      self.timestamp.month,
                                      self.timestamp.day,
                                      13, 00, 0, 0, tzinfo=self.timestamp.tzinfo)
        return start_range < self.timestamp <= end_range

    def __str__(self):
        if self.working:
            return f'Login at {str(self.timestamp.time())}'
        return f'Logout at {str(self.timestamp.time())}'
