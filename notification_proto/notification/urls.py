from django.conf.urls import url

from . import views

app_name = 'notification'
urlpatterns = [
    url(r'^create', views.NotificationCreateView.as_view(), name='create'),
    url(r'^show', views.NotificationShowView.as_view(), name='show')
]
