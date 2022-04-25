# Generated by Django 4.0.1 on 2022-04-25 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_user_first_name_user_last_name_alter_user_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='newInteractedWith',
            field=models.ManyToManyField(related_name='readers_interacted', to='news.News', verbose_name='News User Interacted With'),
        ),
        migrations.AlterField(
            model_name='user',
            name='newsSeen',
            field=models.ManyToManyField(related_name='readers', to='news.News', verbose_name='News Seen By User'),
        ),
    ]
