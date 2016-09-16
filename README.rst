Django-Directmessages
=====================

.. image:: https://travis-ci.org/dmonn/django-directmessages.svg?branch=master
    :target: https://travis-ci.org/dmonn/django-directmessages

Django-Directmessages is a low-level and easy-to-use Django App to manage simple directmessages.
In contrast to other Django Apps for messaging, Django-Directmessages doesn't use any type of pre-built templates and is concentrated on the programmatic usage.

Django-Directmessage is thought to be used with APIs or small apps, but can be used for any type of messaging. It featues:

* Sending of private 1-to-1 messages between users.
* Listing unread messages for a given user.
* Read a given message 
* Get all conversation partners/contacted users for a given user
* Read a whole conversation between two users.

Requirements
============

*Django >= 1.5* is supported

Installation
============

1. ``pip install django-directmessages``
2. add ``"directmessages"`` to ``INSTALLED_APPS`` and run ``python manage.py migrate``.

Usage
=====

Import the Message Management API on top of your ``views.py`` ::

	from directmessages.apps import Inbox

* Send message: ``Inbox.send_message(from_user, to_user, message)``
* List all unread messages: ``Inbox.get_unread_messages(user)``
* Read a message (and mark as read): ``Inbox.read_message(message)``
* Print a message as <user>: <message>: ``Inbox.read_message_formatted(message)``
* Print a list of all conversation partners for a user: ``Inbox.get_conversations(users)``
* Get a conversation between two users: ``Inbox.get_conversation(user1, user2, _limit_, _reversed_, _mark_read_)``
	- Limit (Int: optional): Instead of getting the whole conversation, get the first 50 (depends on reversed)
	- Reversed (Bool: optional): Usually the 'limit'-param gives back the first x messages, if you put Reversed to True, limit will give back the x latest messages.
	- Mark_Read (Bool: optional): Mark all messages in conversation as read

Signals
=======

You can use the following signals to extend the app for your needs

* message_sent:
	Gets called as soon as a message is sent.
	Provides the Message object, the sender and the recipient as params.

* message_read:
	Gets called as soon as a message is read:
	Provides the Message object, the sender and the recipient as params.

Contributing
============

Bug reports, patches and fixes are always welcome!


To Do
=====

* Add some security functions (e.g checking if user is allowed to read a message)
* Add some custom exceptions (e.g. when no message was found)
