from .apps import Inbox
from .models import Message
from django.contrib.auth.models import User
from django.test import TestCase


class MessageSendTestCase(TestCase):
    def setUp(self):
        self.u1 = User.objects.create(username='someuser')
        self.u2 = User.objects.create(username='someotheruser')

    def test_send_message(self):
        init_value = Message.objects.all().count()

        message, status = Inbox.send_message(self.u1, self.u2, "This is a message")

        after_value = Message.objects.all().count()

        self.assertEqual(init_value + 1, after_value)
        self.assertEqual(status, 200)
        self.assertEqual(message.content, "This is a message")


class MessageReadingTestCase(TestCase):
    def setUp(self):
        self.u1 = User.objects.create(username='someuser')
        self.u2 = User.objects.create(username='someotheruser')

    def test_unread_messages(self):
        Inbox.send_message(self.u1, self.u2, "This is a message")

        unread_messages = Inbox.get_unread_messages(self.u1)
        unread_messages2 = Inbox.get_unread_messages(self.u2)

        self.assertEqual(unread_messages.count(), 0)
        self.assertEqual(unread_messages2.count(), 1)

    def test_reading_messages(self):
        Inbox.send_message(self.u2, self.u1, "This is another message")

        unread_messages = Inbox.get_unread_messages(self.u1)
        self.assertEqual(unread_messages.count(), 1)

        message = Inbox.read_message(unread_messages[0].id)
        unread_messages_after = Inbox.get_unread_messages(self.u1)

        self.assertEqual(message, "This is another message")
        self.assertEqual(unread_messages_after.count(), 0)

    def test_reading_formatted(self):
        message, status = Inbox.send_message(self.u2, self.u1, "This is just another message")

        unread_messages = Inbox.get_unread_messages(self.u1)
        self.assertEqual(unread_messages.count(), 1)

        message = Inbox.read_message_formatted(message.id)
        unread_messages_after = Inbox.get_unread_messages(self.u1)

        self.assertEqual(message, self.u2.username + ": This is just another message")
        self.assertEqual(unread_messages_after.count(), 0)


class ConversationTestCase(TestCase):
    def setUp(self):
        self.u1 = User.objects.create(username='User')
        self.u2 = User.objects.create(username='Admin')
        self.u3 = User.objects.create(username='Postman')
        self.u4 = User.objects.create(username='Chef')

        # Sender U1
        Inbox.send_message(self.u1, self.u2, "This is a message to User 2")
        Inbox.send_message(self.u1, self.u3, "This is a message to User 3")
        Inbox.send_message(self.u1, self.u4, "This is a message to User 4")

        # Sender U2
        Inbox.send_message(self.u2, self.u1, "This is a message to User 1")
        Inbox.send_message(self.u2, self.u3, "This is a message to User 3")
        Inbox.send_message(self.u2, self.u4, "This is a message to User 4")

        # Some more message between U1 and U2
        Inbox.send_message(self.u1, self.u2, "Hey, thanks for sending this message back")
        Inbox.send_message(self.u2, self.u1, "No problem")

    def test_all_conversations(self):
        conversation_partners = Inbox.get_conversations(self.u1)

        self.assertEqual(len(conversation_partners), 3)
        self.assertIn(self.u2, conversation_partners)
        self.assertIn(self.u3, conversation_partners)
        self.assertIn(self.u4, conversation_partners)

        self.assertNotIn(self.u1, conversation_partners)

    def test_single_conversation(self):
        unread_messages = Inbox.get_unread_messages(self.u1)

        self.assertEqual(unread_messages.count(), 2)

        conversation = Inbox.get_conversation(self.u1, self.u2)
        unread_messages_after = Inbox.get_unread_messages(self.u1)

        self.assertEqual(conversation.count(), 4)
        self.assertEqual(unread_messages_after.count(), 2)

        conversation_limited = Inbox.get_conversation(self.u1, self.u2, limit=2, reversed=True)
        self.assertEqual(conversation_limited.count(), 2)

        self.assertEqual(conversation[0].content, "This is a message to User 2")
        self.assertEqual(conversation[len(conversation) - 1].content, "No problem")
        self.assertEqual(conversation_limited[0].content, "No problem")
        self.assertEqual(conversation_limited[len(conversation_limited) - 1].content,
                         "Hey, thanks for sending this message back")
