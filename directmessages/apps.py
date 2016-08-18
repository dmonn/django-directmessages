from __future__ import unicode_literals
from django import VERSION as DJANGO_VERSION

Inbox = None

if DJANGO_VERSION >= (1, 7):
    from django.apps import AppConfig
    class DirectmessagesConfig(AppConfig):
        name = 'directmessages'
        label = 'directmessaging'

        def ready(self):
            # For convenience
            from directmessages.services import MessagingService
            global Inbox
            Inbox = MessagingService()

else:
    def populateInbox():
        from directmessages.services import MessagingService
        global Inbox
        Inbox = MessagingService()
