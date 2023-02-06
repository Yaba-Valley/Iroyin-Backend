# Generated by Django 4.0.1 on 2023-02-06 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_news_time_added'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='liked_news',
            field=models.ManyToManyField(related_name='likers', to='news.News', verbose_name='news liked'),
        ),
        migrations.AddField(
            model_name='user',
            name='saved_news',
            field=models.ManyToManyField(related_name='savers', to='news.News', verbose_name='news saved'),
        ),
        migrations.AddField(
            model_name='user',
            name='shared_news',
            field=models.ManyToManyField(related_name='sharers', to='news.News', verbose_name='news shared'),
        ),
    ]
