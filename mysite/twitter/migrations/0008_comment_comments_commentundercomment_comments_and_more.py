# Generated by Django 4.2.4 on 2023-08-09 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0007_alter_comment_likes_alter_commentundercomment_likes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comments',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='commentundercomment',
            name='comments',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='comments',
            field=models.IntegerField(default=0),
        ),
    ]
