from django.db import models
from django.db.models import Q, F
from django.contrib.auth import get_user_model

User = get_user_model()

MAX_TWEETS_HISTORY = 5

def convert_delta_time(dt, dt_now):
	delta_time = dt_now - dt

	if delta_time.days > 0 :
		return dt.strftime('%b %d')
	elif delta_time.seconds // 3600 > 0 :
		return str(delta_time.seconds // 3600) + 'h'
	elif delta_time.seconds // 60 > 0 :
		return str(delta_time.seconds // 60) + 'm'
	else :
		return 'Now'


# Create your models here.

class Tweet(models.Model):
	owner						= models.ForeignKey(User, null=False, on_delete=models.CASCADE)

	description			= models.TextField(max_length=1024, blank=True)
	picture 				= models.ImageField(upload_to='tweet_pic/', null=True, blank=True)
	timestamp				= models.DateTimeField(auto_now_add=True)

	like 						= models.ManyToManyField(User, blank=True, related_name='liked_tweets')
	retweet 				= models.ManyToManyField(User, blank=True, related_name='retweeted_tweets')

	related_users 	= models.ManyToManyField(User, blank=True, related_name='history')

	like_count			= models.IntegerField(default=0)
	retweet_count		= models.IntegerField(default=0)
	comment_count		= models.IntegerField(default=0)

	def __str__(self):
		return self.owner.get_full_name() + ' tweet\'s'

	def push_tweet_history(self, user):
			self.related_users.add(user)
			if user.history.count() > MAX_TWEETS_HISTORY:
				user.history.remove(user.history.first())

	def share_tweet_followers(self):
		self.push_tweet_history(self.owner)
		for fw in self.owner.follower.all():
			self.push_tweet_history(fw)

	def is_liked(self, user):
		return self.like.filter(pk=user.pk).exists()

	def is_retweeted(self, user):
		return self.retweet.filter(pk=user.pk).exists()

	def toggle_like(self, user):
		if self.is_liked(user):
			self.like.remove(user)
			self.like_count = F('like_count') - 1
			self.save()
			return False
		else:
			self.like.add(user)
			self.like_count = F('like_count') + 1
			self.save()
			return True

	def toggle_retweet(self, user):
		if self.is_retweeted(user):
			self.retweet.remove(user)
			self.retweet_count = F('retweet_count') - 1
			self.save()
			return False
		else:
			self.retweet.add(user)
			self.retweet_count = F('retweet_count') + 1
			self.save()
			return True

	def comment_added(self):
		self.comment_count = F('comment_count') + 1
		self.save()

	def comment_deleted(self):
		self.comment_count = F('comment_count') - 1
		self.save()

class Comment(models.Model):
	owner						= models.ForeignKey(User, null=False, related_name='commented', on_delete=models.CASCADE)

	tweet 					= models.ForeignKey(Tweet, null=False, related_name='comments', on_delete=models.CASCADE)

	comment 				= models.TextField(max_length=1024)

	def __str__(self):
		return self.owner.get_full_name() + ' comment\'s'