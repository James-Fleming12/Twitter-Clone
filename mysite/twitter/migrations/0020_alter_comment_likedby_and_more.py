# Generated by Django 4.2.3 on 2023-08-15 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0019_postlist_description_alter_comment_likedby_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='likedBy',
            field=models.ManyToManyField(related_name='comment_like', to='twitter.user2'),
        ),
        migrations.AlterField(
            model_name='commentundercomment',
            name='likedBy',
            field=models.ManyToManyField(related_name='commentplus_like', to='twitter.user2'),
        ),
        migrations.AlterField(
            model_name='post',
            name='likedBy',
            field=models.ManyToManyField(related_name='post_like', to='twitter.user2'),
        ),
        migrations.AlterField(
            model_name='postlist',
            name='posts',
            field=models.ManyToManyField(related_name='listed_post', to='twitter.post'),
        ),
        migrations.AlterField(
            model_name='user2',
            name='bookmarks',
            field=models.ManyToManyField(related_name='bookmarked_post', to='twitter.post'),
        ),
        migrations.AlterField(
            model_name='user2',
            name='following',
            field=models.ManyToManyField(related_name='follow_account', to='twitter.followobj'),
        ),
        migrations.AlterField(
            model_name='user2',
            name='ownlists',
            field=models.ManyToManyField(related_name='own_list', to='twitter.postlist'),
        ),
        migrations.AlterField(
            model_name='user2',
            name='savedlists',
            field=models.ManyToManyField(related_name='saved_list', to='twitter.postlist'),
        ),
    ]