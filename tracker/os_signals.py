import logging

import dbus
import gobject
from dbus.mainloop.glib import DBusGMainLoop

from tracker.models import Session, Event

logging.basicConfig()

logger = logging.getLogger(__name__)

dbus_loop = DBusGMainLoop(set_as_default=True)


def message_callback(bus, message):
    if message.get_interface() == "org.gnome.ScreenSaver":
        if message.get_member() == "ActiveChanged":
            screensaver_enabled = bool(message.get_args_list()[0])
            session, created = Session.objects.get_or_create()
            Event.objects.create(session=session, working=not screensaver_enabled)


session = dbus.SessionBus(mainloop=dbus_loop)
session.add_match_string_non_blocking("interface='org.gnome.ScreenSaver'")

session.add_message_filter(message_callback)

logger.info("Starting up.")

loop = gobject.MainLoop()
loop.run()
