from django.dispatch import Signal

message_sent = Signal(providing_args=['from_user', 'to'])
message_read = Signal(providing_args=['from_user', 'to'])