from django.db import models
from django.conf import settings

class Message(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authored_messages')
    # We can use a generic relation or a specific FK to a chat room model later.
    # For now, let's assume a chat is tied to an order.
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='chat_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.author.username} at {self.timestamp}'

    class Meta:
        ordering = ['timestamp']
