from rest_framework import serializers
from rest_framework.reverse import reverse
from news_app.models import Tweet, Comment, convert_delta_time
from user_app.models import DEFAULT_USER_PIC_URI
from user_app.serializers import SoftUserSerializer
from datetime import datetime, timezone

class TweetSerializer(serializers.ModelSerializer):
	url 						= serializers.HyperlinkedIdentityField(view_name='news:tweet_detail')

	owner						= SoftUserSerializer(read_only=True)

	likes 					= serializers.ReadOnlyField()
	retweets 				= serializers.ReadOnlyField()
	comments 				= serializers.ReadOnlyField()

	like_count 			= serializers.IntegerField(read_only=True)
	retweet_count 	= serializers.IntegerField(read_only=True)
	comment_count 	= serializers.IntegerField(read_only=True)

	is_liked				= serializers.BooleanField(default=False, read_only=True)
	is_retweeted		= serializers.BooleanField(default=False, read_only=True)

	class Meta:
		model = Tweet
		fields = ['id', 'url', 'owner', 'description', 'picture', 'timestamp', 'like_count', 'retweet_count', 'comment_count', 'likes', 'retweets', 'comments', 'is_liked', 'is_retweeted']

	def validate(self, data):
		if (data['description'] == '') and not(('picture' in data) and data['picture']):
			raise serializers.ValidationError('Tweet must have a description or/and a picture')
		return data

	def to_representation(self, instance):
		representation 									= super(TweetSerializer, self).to_representation(instance)
		request 												= self.context['request']
		user 														= request.user
		representation['timestamp']			= convert_delta_time(instance.timestamp, datetime.now(timezone.utc))
		representation['likes']					= reverse('news:toggle_like', args=[instance.id,], request=request)
		representation['retweets']			= reverse('news:toggle_retweet', args=[instance.id,], request=request)
		representation['comments']			= reverse('news:comment_list', args=[instance.id,], request=request)
		representation['is_liked']			= instance.is_liked(user)
		representation['is_retweeted']	= instance.is_retweeted(user)
		return representation


class CommentSerializer(serializers.ModelSerializer):
	url 						= serializers.HyperlinkedIdentityField(view_name='news:comment_detail')

	owner 					= serializers.HyperlinkedRelatedField(read_only=True, view_name='user:user_detail')

	tweet 					= serializers.HyperlinkedRelatedField(read_only=True, view_name='news:tweet_detail')

	class Meta:
		model = Comment
		fields = ['id', 'url', 'owner', 'tweet', 'comment']