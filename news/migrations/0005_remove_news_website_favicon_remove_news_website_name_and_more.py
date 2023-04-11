# Generated by Django 4.0.1 on 2023-04-11 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_news_entities'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='website_favicon',
        ),
        migrations.RemoveField(
            model_name='news',
            name='website_name',
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('general_name', models.CharField(max_length=500, verbose_name='Name')),
                ('sub_category', models.CharField(max_length=100)),
                ('website_favicon', models.URLField(default='https://media.istockphoto.com/vectors/news-vector-id918880270?k=20&m=918880270&s=612x612&w=0&h=bDcgr9jhiRYCPMUhVdLKD5ouIc5daM4qMcaPPapppQI=', verbose_name='Favicon')),
                ('website_url', models.URLField(verbose_name='URL')),
                ('smallest_article_element', models.CharField(default='', max_length=10, verbose_name='News Container HTML Element')),
                ('class_of_smallest_article_element', models.CharField(default='', max_length=500, verbose_name='Class of News Container HTML Element')),
                ('smallest_link_element', models.CharField(default='', max_length=10, verbose_name='News Link HTML Element')),
                ('class_of_smallest_link_element', models.CharField(default='', max_length=500, verbose_name='Class of News Link HTML Element')),
                ('smallest_image_element', models.CharField(default='', max_length=10, verbose_name='News Image HTML Element')),
                ('class_of_smallest_image_element', models.CharField(default='', max_length=500, verbose_name='Class of News Image HTML Element')),
                ('smallest_title_element', models.CharField(default='', max_length=10, verbose_name='News title HTML Element')),
                ('class_of_smallest_title_element', models.CharField(default='', max_length=500, verbose_name='Class of News title HTML Element')),
                ('image_holder_attr', models.CharField(default='src', max_length=500, verbose_name='Image Holder Attribute (src,data-src,srcset,etc.)')),
                ('preprend_image_url', models.CharField(default='', max_length=500, verbose_name='Prepend Image URL')),
                ('prepend_news_url', models.CharField(default='', max_length=500, verbose_name='Prepend News URL')),
                ('categories', models.ManyToManyField(related_name='websites', to='news.Interest', verbose_name='Categories')),
            ],
        ),
        migrations.AddField(
            model_name='news',
            name='website',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='news', to='news.website'),
        ),
    ]
