# Generated by Django 4.2.3 on 2023-08-17 02:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0020_alter_comment_likedby_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('postUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postuser', to='twitter.user2')),
                ('recieveUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recieveuser', to='twitter.user2')),
            ],
        ),
        migrations.AddField(
            model_name='user2',
            name='notificationlist',
            field=models.ManyToManyField(related_name='notifications', to='twitter.notification'),
        ),
    ]
