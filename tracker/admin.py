from django.contrib import admin

from tracker.models import Session, Event


class EvenInline(admin.TabularInline):
    model = Event
    extra = 0
    ordering = ['timestamp']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    inlines = [
        EvenInline,
    ]
