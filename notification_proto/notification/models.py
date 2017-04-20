from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    create_time = models.DateTimeField('date created', auto_now_add=True)
    sender = models.ForeignKey(User, related_name='note_sent')
    receiver = models.ForeignKey(User, related_name='note_received')
    content = models.CharField(max_length=150, default='', verbose_name='信件內容')

    def __str__(self):
        return '發送者: {}, 接收者:{}, 時間:{}, 內容:{}'.format(
        	self.sender, self.receiver, self.create_time, self.content)
