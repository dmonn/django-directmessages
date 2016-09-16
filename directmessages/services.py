from __future__ import unicode_literals

from .models import Message
from .signals import message_read, message_sent
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q


class MessagingService(object):
    """
    A object to manage all messages and conversations
    """

    # Message creation

    def send_message(self, sender, recipient, message):
        """
        Send a new message
        :param sender: user
        :param recipient: user
        :param message: String
        :return: Message and status code
        """

        if sender == recipient:
            raise ValidationError("You can't send messages to yourself.")

        message = Message(sender=sender, recipient=recipient, content=str(message))
        message.save()

        message_sent.send(sender=message, from_user=message.sender, to=message.recipient)

        # The second value acts as a status value
        return message, 200

    # Message reading
    def get_unread_messages(self, user):
        """
        List of unread messages for a specific user
        :param user: user
        :return: messages
        """
        return Message.objects.all().filter(recipient=user, read_at=None)

    def read_message(self, message_id):
        """
        Read specific message
        :param message_id: Integer
        :return: Message Text
        """
        try:
            message = Message.objects.get(id=message_id)
            self.mark_as_read(message)
            return message.content
        except Message.DoesNotExist:
            return ""

    def read_message_formatted(self, message_id):
        """
        Read a message in the format <User>: <Message>
        :param message_id: Id
        :return: Formatted Message Text
        """
        try:
            message = Message.objects.get(id=message_id)
            self.mark_as_read(message)
            return message.sender.username + ": "+message.content
        except Message.DoesNotExist:
            return ""

    # Conversation management

    def get_conversations(self, user):
        """
        Lists all conversation-partners for a specific user
        :param user: User
        :return: Conversation list
        """
        all_conversations = Message.objects.all().filter(Q(sender=user) | Q(recipient=user))

        contacts = []
        for conversation in all_conversations:
            if conversation.sender != user:
                contacts.append(conversation.sender)
            elif conversation.recipient != user:
                contacts.append(conversation.recipient)

        # To abolish duplicates
        return list(set(contacts))

    def get_conversation(self, user1, user2, limit=None, reversed=False, mark_read=False):
        """
        List of messages between two users
        :param user1: User
        :param user2: User
        :param limit: int
        :param reversed: Boolean - Makes the newest message be at index 0
        :return: messages
        """
        users = [user1, user2]

        # Newest message first if it's reversed (index 0)
        if reversed:
            order = '-pk'
        else:
            order = 'pk'

        conversation = Message.objects.all().filter(sender__in=users, recipient__in=users).order_by(order)

        if limit:
            # Limit number of messages to the x newest
            conversation = conversation[:limit]

        if mark_read:
            for message in conversation:
                # Just to be sure, everything is read
                self.mark_as_read(message)

        return conversation

    # Helper methods
    def mark_as_read(self, message):
        """
        Marks a message as read, if it hasn't been read before
        :param message: Message
        """

        if message.read_at is None:
            message.read_at = timezone.now()
            message_read.send(sender=message, from_user=message.sender, to=message.recipient)
            message.save()

