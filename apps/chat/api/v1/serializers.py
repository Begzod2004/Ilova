from rest_framework import serializers
from apps.chat.models import ChatModel


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatModel
        fields = ('id', "sender", "reciver", "message", "is_read", "date_created")
        

    