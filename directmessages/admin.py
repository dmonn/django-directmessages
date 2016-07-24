from .models import Message
from django.contrib import admin

class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ('id', 'sender', 'recipient', 'content', )

admin.site.register(Message, MessageAdmin)