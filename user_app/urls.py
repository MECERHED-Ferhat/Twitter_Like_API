from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from user_app import views

app_name = 'user'

urlpatterns = format_suffix_patterns([
	path('', views.UserList.as_view(), name="user_list"),
	path('<str:pk>', views.UserDetail.as_view(), name="user_detail"),

	path('detail/<str:pk>', views.HardUserDetail.as_view(), name="hard_user_detail"),

	path('followers/<str:pk>', views.FollowerUserList.as_view(), name="follower_user_list"),
	path('following/<str:pk>', views.FollowingUserList.as_view(), name="following_user_list"),
	path('toggleFollow/<str:pk>', views.ToggleFollowView.as_view(), name="toggle_follow"),

	path('search/', views.UserSearch.as_view(), name="user_search"),
])