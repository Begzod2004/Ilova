from django.db import models
from apps.account.models import Account, SimpleUser
from apps.contact.models import Communication

class Chat(models.Model):
    communication = models.ForeignKey(Communication, on_delete=models.CASCADE, related_name='chat')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='chat_from')
    is_user = models.BooleanField()
    message = models.TextField()
    file = models.FileField(upload_to='chatmedia')
    is_read = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'{self.is_user} {self.message[:30]}'


class ChatModel(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name="Sender")
    reciver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="Reciver")
    message = models.CharField(max_length=221)
    is_read = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"sender {self.message}"