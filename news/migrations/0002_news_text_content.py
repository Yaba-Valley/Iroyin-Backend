# Generated by Django 4.0.1 on 2023-01-18 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='text_content',
            field=models.TextField(default=''),
        ),
    ]
