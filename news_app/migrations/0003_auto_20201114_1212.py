# Generated by Django 3.1.3 on 2020-11-14 11:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news_app', '0002_auto_20201113_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='related_users',
            field=models.ManyToManyField(blank=True, related_name='history', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='TweetHistory',
        ),
    ]
