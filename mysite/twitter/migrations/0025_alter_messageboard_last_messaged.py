# Generated by Django 4.2.3 on 2023-09-24 23:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0024_remove_messageboard_user1_remove_messageboard_user2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messageboard',
            name='last_messaged',
            field=models.DateTimeField(verbose_name='last message'),
        ),
    ]
