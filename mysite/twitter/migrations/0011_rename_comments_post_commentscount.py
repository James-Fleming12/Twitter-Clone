# Generated by Django 4.2.4 on 2023-08-09 23:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0010_post_likedby_delete_postlike'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='comments',
            new_name='commentsCount',
        ),
    ]
