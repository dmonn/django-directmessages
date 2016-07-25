from __future__ import unicode_literals

from directmessages.services import MessagingService
from django.apps import AppConfig


class DirectmessagesConfig(AppConfig):
    name = 'directmessages'

    def ready(self):
        # For convenience
        Inbox = MessagingService()