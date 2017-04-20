from django.shortcuts import render
from .models import Notification
# Create your views here.
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView


class NotificationCreateView(CreateView):
    model = Notification
    fields = ['sender', 'receiver', 'content']
    template_name = 'notification/create.html'
    success_url = '/notification/create'


class NotificationShowView(ListView):
	model = Notification
	template_name = "notification/show.html"
