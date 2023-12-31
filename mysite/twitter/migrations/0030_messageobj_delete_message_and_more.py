# Generated by Django 4.2.3 on 2023-09-28 23:20

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0029_remove_message_board_message_time_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageObj',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('time', models.DateTimeField(default=datetime.datetime(2023, 9, 28, 23, 20, 54, 338046, tzinfo=datetime.timezone.utc), verbose_name='sent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='twitter.user2')),
            ],
        ),
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.AlterField(
            model_name='messageboard',
            name='messages',
            field=models.ManyToManyField(related_name='messages', to='twitter.messageobj'),
        ),
    ]
