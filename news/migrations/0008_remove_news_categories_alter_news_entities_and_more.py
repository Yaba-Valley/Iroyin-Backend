# Generated by Django 4.0.1 on 2023-04-11 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_alter_website_class_of_smallest_article_element_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='categories',
        ),
        migrations.AlterField(
            model_name='news',
            name='entities',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='news',
            name='text_content',
            field=models.TextField(blank=True, default=''),
        ),
    ]
