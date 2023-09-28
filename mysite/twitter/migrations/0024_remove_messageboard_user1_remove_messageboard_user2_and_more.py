# Generated by Django 4.2.3 on 2023-09-24 22:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0023_messageboard_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messageboard',
            name='user1',
        ),
        migrations.RemoveField(
            model_name='messageboard',
            name='user2',
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='twitter.user2'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='messageboard',
            name='last_messaged',
            field=models.DateTimeField(verbose_name='last message'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='messageboard',
            name='name',
            field=models.CharField(default='name', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='messageboard',
            name='users',
            field=models.ManyToManyField(null=True, related_name='users', to='twitter.user2'),
        ),
        migrations.AlterField(
            model_name='message',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='board', to='twitter.messageboard'),
        ),
    ]