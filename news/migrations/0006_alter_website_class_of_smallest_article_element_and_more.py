# Generated by Django 4.0.1 on 2023-04-11 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_remove_news_website_favicon_remove_news_website_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='class_of_smallest_article_element',
            field=models.CharField(max_length=500, null=True, verbose_name='Class of News Container HTML Element'),
        ),
        migrations.AlterField(
            model_name='website',
            name='class_of_smallest_image_element',
            field=models.CharField(max_length=500, null=True, verbose_name='Class of News Image HTML Element'),
        ),
        migrations.AlterField(
            model_name='website',
            name='class_of_smallest_link_element',
            field=models.CharField(max_length=500, null=True, verbose_name='Class of News Link HTML Element'),
        ),
        migrations.AlterField(
            model_name='website',
            name='class_of_smallest_title_element',
            field=models.CharField(max_length=500, null=True, verbose_name='Class of News title HTML Element'),
        ),
    ]
