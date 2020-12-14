from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth import get_user_model
from user_app.models import DEFAULT_USER_PIC_URI

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
	url 						= serializers.HyperlinkedIdentityField(read_only=True, view_name='user:user_detail')

	full_name 			= serializers.CharField(read_only=True)


	class Meta:
		model = User
		fields = ['url', 'username', 'email', 'full_name', 'last_name', 'first_name', 'picture']

	def to_representation(self, instance):
		representation 								= super(UserSerializer, self).to_representation(instance)
		representation['full_name']		= instance.get_full_name()
		if not instance.picture :
			representation['picture']		= self.context['request'].build_absolute_uri(DEFAULT_USER_PIC_URI)
		return representation




class SoftUserSerializer(serializers.ModelSerializer):
	url 						= serializers.HyperlinkedIdentityField(read_only=True, view_name='user:user_detail')

	full_name 			= serializers.CharField(read_only=True)

	is_current			= serializers.BooleanField(read_only=True)

	class Meta:
		model = User
		fields = ['url', 'username', 'full_name', 'picture', 'is_current']

	def to_representation(self, instance):
		representation 								= super(SoftUserSerializer, self).to_representation(instance)
		representation['full_name'] 	= instance.get_full_name()
		representation['is_current']	= instance == self.context['request'].user
		if not instance.picture:
			representation['picture'] 	= self.context['request'].build_absolute_uri(DEFAULT_USER_PIC_URI)
		return representation



class HardUserSerializer(serializers.ModelSerializer):
	url 						= serializers.HyperlinkedIdentityField(read_only=True, view_name='user:user_detail')

	full_name 			= serializers.CharField(read_only=True)

	following				= serializers.ReadOnlyField()

	followers				= serializers.ReadOnlyField()

	follower_count 	= serializers.IntegerField(read_only=True)

	following_count = serializers.IntegerField(read_only=True)

	tweet_count			= serializers.IntegerField(read_only=True)

	is_current 			= serializers.BooleanField(read_only=True)

	is_following		= serializers.BooleanField(read_only=True)

	follow_url			= serializers.ReadOnlyField()

	tweet_url				= serializers.ReadOnlyField()


	class Meta:
		model = User
		fields = ['url', 'username', 'full_name', 'picture', 'timestamp', 'following', 'followers', 'following_count', 'follower_count', 'tweet_count', 'is_current', 'is_following', 'follow_url', 'tweet_url']

	def to_representation(self, instance):
		user 																= self.context['request'].user
		is_current													= instance == user
		representation 											= super(HardUserSerializer, self).to_representation(instance)
		representation['full_name']					= instance.get_full_name()
		representation['timestamp']					= instance.timestamp.strftime('%b %Y')
		representation['followers']					= reverse('user:follower_user_list', args=[instance.pk,], request=self.context['request'])
		representation['following']					= reverse('user:following_user_list', args=[instance.pk,], request=self.context['request'])
		representation['following_count'] 	= instance.follow.count()
		representation['follower_count']		= instance.follower.count()
		representation['tweet_count']				= instance.tweet_set.count()
		representation['is_current']				= is_current
		representation['is_following']			= (not is_current) and instance.is_followed(user)
		representation['follow_url']				= reverse('user:toggle_follow', args=[instance.pk,], request=self.context['request'])
		representation['tweet_url']					= reverse('news:user_tweet_list', args=[instance.pk,], request=self.context['request'])
		if not instance.picture :
			representation['picture']					= self.context['request'].build_absolute_uri(DEFAULT_USER_PIC_URI)
		return representation



class FollowUserSerializer(serializers.ModelSerializer):
	url 					= serializers.HyperlinkedIdentityField(read_only=True, view_name='user:user_detail')

	full_name 		= serializers.CharField(read_only=True)

	is_current		= serializers.BooleanField(read_only=True)

	is_following	= serializers.BooleanField(read_only=True)

	follow_url 		= serializers.ReadOnlyField()

	class Meta:
		model = User
		fields = ['url', 'username', 'full_name', 'picture', 'is_following', 'is_current', 'follow_url']

	def to_representation(self, instance):
		user 																= self.context['request'].user
		is_current													= (user == instance)
		representation 											= super(FollowUserSerializer, self).to_representation(instance)
		representation['full_name']					= instance.get_full_name()
		representation['is_current']				= is_current
		representation['is_following']			= (not is_current) and instance.is_followed(user)
		representation['follow_url']				= reverse('user:toggle_follow', args=[instance.pk,], request=self.context['request'])
		if not instance.picture:
			representation['picture']					= self.context['request'].build_absolute_uri(DEFAULT_USER_PIC_URI)
		return representation
