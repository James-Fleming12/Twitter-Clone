# Generated by Django 4.2.3 on 2023-09-28 04:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0028_alter_message_board_alter_message_text_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='board',
        ),
        migrations.AddField(
            model_name='message',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 28, 4, 36, 45, 784522, tzinfo=datetime.timezone.utc), verbose_name='sent'),
        ),
        migrations.AddField(
            model_name='messageboard',
            name='messages',
            field=models.ManyToManyField(related_name='messages', to='twitter.message'),
        ),
    ]
