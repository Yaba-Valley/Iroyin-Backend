# Generated by Django 4.0.1 on 2023-02-12 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_news_time_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='entities',
            field=models.TextField(default=''),
        ),
    ]
