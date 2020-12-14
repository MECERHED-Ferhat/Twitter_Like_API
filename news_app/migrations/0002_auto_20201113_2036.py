# Generated by Django 3.1.3 on 2020-11-13 19:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='liked_tweets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tweet',
            name='retweet',
            field=models.ManyToManyField(blank=True, related_name='retweeted_tweets', to=settings.AUTH_USER_MODEL),
        ),
    ]