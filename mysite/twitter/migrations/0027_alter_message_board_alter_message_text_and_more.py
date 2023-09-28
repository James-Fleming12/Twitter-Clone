# Generated by Django 4.2.3 on 2023-09-24 23:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0026_alter_messageboard_last_messaged'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='board',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='board', to='twitter.messageboard'),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='twitter.user2'),
        ),
        migrations.AlterField(
            model_name='messageboard',
            name='last_messaged',
            field=models.DateTimeField(null=True, verbose_name='last message'),
        ),
        migrations.AlterField(
            model_name='messageboard',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]