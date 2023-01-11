# Generated by Django 4.0.1 on 2023-01-11 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=False)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=100, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=100, verbose_name='Last Name')),
                ('interests', models.ManyToManyField(related_name='users', to='news.Interest')),
                ('newInteractedWith', models.ManyToManyField(related_name='readers_interacted', to='news.News', verbose_name='News User Interacted With')),
                ('newsSeen', models.ManyToManyField(related_name='readers', to='news.News', verbose_name='News Seen By User')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]