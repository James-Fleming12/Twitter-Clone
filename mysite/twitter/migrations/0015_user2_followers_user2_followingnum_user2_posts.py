# Generated by Django 4.2.3 on 2023-08-15 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0014_comment_likedby_commentundercomment_likedby'),
    ]

    operations = [
        migrations.AddField(
            model_name='user2',
            name='followers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user2',
            name='followingNum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user2',
            name='posts',
            field=models.IntegerField(default=0),
        ),
    ]
