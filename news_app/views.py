from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from news_app.models import Tweet, Comment
from news_app.serializers import TweetSerializer, CommentSerializer
from news_app.permissions import IsOwnerOrReadOnly

User = get_user_model()

class TweetList(generics.ListCreateAPIView):
	serializer_class	= TweetSerializer

	permission_classes = [
		permissions.IsAuthenticated,
	]

	def get_queryset(self):
		user = self.request.user
		return user.tweet_set.all().order_by('-timestamp')

	def perform_create(self, serializer):
		tweet = serializer.save(owner=self.request.user)
		tweet.share_tweet_followers()

class TweetDetail(generics.RetrieveUpdateDestroyAPIView):
	serializer_class	= TweetSerializer
	queryset = Tweet.objects.all()

	permission_classes = [
		permissions.IsAuthenticated,
		IsOwnerOrReadOnly,
	]



class TweetHistoryList(generics.ListAPIView):
	serializer_class = TweetSerializer

	permission_classes = [
		permissions.IsAuthenticated,
	]

	def get_queryset(self):
		user = self.request.user
		return user.history.all().order_by('-timestamp')


class UserTweetList(generics.ListAPIView):
	serializer_class = TweetSerializer

	permission_classes = [
		permissions.IsAuthenticated,
	]

	def get_queryset(self):
		user = get_object_or_404(User, pk=self.kwargs['user'])
		return user.tweet_set.all()



class CommentList(generics.ListCreateAPIView):
	serializer_class = CommentSerializer

	permission_classes = [
		permissions.IsAuthenticated,
	]

	def get_queryset(self):
		tweet = get_object_or_404(Tweet, pk=self.kwargs['tweet'])
		return tweet.comments.all()

	def perform_create(self, serializer):
		tweet = get_object_or_404(Tweet, pk=self.kwargs['tweet'])
		comment = serializer.save(owner=self.request.user, tweet=tweet)
		comment.tweet.comment_added()

class CommentDetail(generics.RetrieveDestroyAPIView):
	serializer_class = CommentSerializer
	queryset = Comment.objects.all()

	permission_classes = [
		permissions.IsAuthenticated,
		IsOwnerOrReadOnly,
	]

	def perform_destroy(self, instance):
		instance.tweet.comment_deleted()
		instance.delete()



class ToggleLikeView(APIView):

	permission_classes = [
		permissions.IsAuthenticated,
	]

	def put(self, request, pk, format=None):
		tweet = get_object_or_404(Tweet, pk=pk)
		
		return Response({'result' : tweet.toggle_like(request.user)})

class ToggleRetweetView(APIView):

	permission_classes = [
		permissions.IsAuthenticated,
	]

	def put(self, request, pk, format=None):
		tweet = get_object_or_404(Tweet, pk=pk)

		return Response({'result' : tweet.toggle_retweet(request.user)})