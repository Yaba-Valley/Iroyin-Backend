# Generated by Django 4.0.1 on 2023-04-11 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_alter_news_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='website',
            name='class_of_smallest_article_element',
            field=models.CharField(blank=True, default='', max_length=500, verbose_name='Class of News Container HTML Element'),
        ),
        migrations.AlterField(
            model_name='website',
            name='class_of_smallest_image_element',
            field=models.CharField(blank=True, default='', max_length=500, verbose_name='Class of News Image HTML Element'),
        ),
        migrations.AlterField(
            model_name='website',
            name='class_of_smallest_link_element',
            field=models.CharField(blank=True, default='', max_length=500, verbose_name='Class of News Link HTML Element'),
        ),
        migrations.AlterField(
            model_name='website',
            name='class_of_smallest_title_element',
            field=models.CharField(blank=True, default='', max_length=500, verbose_name='Class of News title HTML Element'),
        ),
        migrations.AlterField(
            model_name='website',
            name='prepend_news_url',
            field=models.CharField(blank=True, default='', max_length=500, verbose_name='Prepend News URL'),
        ),
        migrations.AlterField(
            model_name='website',
            name='preprend_image_url',
            field=models.CharField(blank=True, default='', max_length=500, verbose_name='Prepend Image URL'),
        ),
    ]
