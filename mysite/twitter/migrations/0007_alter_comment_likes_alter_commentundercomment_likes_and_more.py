# Generated by Django 4.2.4 on 2023-08-09 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0006_rename_user_user2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='commentundercomment',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
