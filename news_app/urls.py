from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from news_app import views

app_name = 'news'

urlpatterns = format_suffix_patterns([
	path('', views.TweetList.as_view(), name="tweet_list"),
	path('<int:pk>', views.TweetDetail.as_view(), name="tweet_detail"),
	
	path('tweetHistory/', views.TweetHistoryList.as_view(), name="tweet_history_list"),
	path('userTweet/<str:user>', views.UserTweetList.as_view(), name="user_tweet_list"),

	path('comments/<int:tweet>', views.CommentList.as_view(), name="comment_list"),
	path('comments/get/<int:pk>', views.CommentDetail.as_view(), name="comment_detail"),

	path('toggleLike/<int:pk>', views.ToggleLikeView.as_view(), name="toggle_like"),
	path('toggleRetweet/<int:pk>', views.ToggleRetweetView.as_view(), name="toggle_retweet"),

])