from __future__ import unicode_literals


from django.apps import AppConfig

Inbox = None

class DirectmessagesConfig(AppConfig):
    name = 'directmessages'
    label = 'somethingelse'

    def ready(self):
        # For convenience
        from directmessages.services import MessagingService
        global Inbox
        Inbox = MessagingService()