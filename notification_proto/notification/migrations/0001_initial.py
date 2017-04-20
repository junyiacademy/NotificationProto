# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-20 15:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('content', models.CharField(default='', max_length=150, verbose_name='信件內容')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='note_received', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='note_sent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]