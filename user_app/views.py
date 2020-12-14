from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import get_object_or_404

from user_app.serializers import UserSerializer, HardUserSerializer, SoftUserSerializer, FollowUserSerializer
from user_app.permissions import IsCurrentUserOrReadOnly

User = get_user_model()

class LoginView(APIView):

	def get(self, request):
		if request.user.is_authenticated :
			user = UserSerializer(request.user, context={'request':request})
			return Response(user.data, status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_401_UNAUTHORIZED)



class UserList(generics.ListCreateAPIView):
	queryset					= User.objects.all()
	serializer_class	= UserSerializer

	permission_classes = [
		permissions.IsAuthenticated,
	]

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset					= User.objects.all()
	serializer_class	= UserSerializer

	permission_classes = [
		permissions.IsAuthenticated,
		IsCurrentUserOrReadOnly,
	]



class ToggleFollowView(APIView):

	permission_classes = [
		permissions.IsAuthenticated,
	]

	def put(self, request, pk, format=None):
		current_user = request.user
		user = get_object_or_404(User, pk=pk)

		if current_user == user:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		return Response({ 'result' : current_user.toggleFollow(user)})


class FollowerUserList(generics.ListAPIView):
	serializer_class = FollowUserSerializer

	permission_classes = [
		permissions.IsAuthenticated,
	]

	def get_queryset(self):
		user = get_object_or_404(User, pk=self.kwargs['pk'])
		return user.follower.all()

class FollowingUserList(generics.ListAPIView):
	serializer_class = FollowUserSerializer

	permission_classes = [
		permissions.IsAuthenticated,
	]

	def get_queryset(self):
		user = get_object_or_404(User, pk=self.kwargs['pk'])
		return user.follow.all()



class HardUserDetail(generics.RetrieveAPIView):
	queryset					= User.objects.all()
	serializer_class	= HardUserSerializer

	permission_classes = [
		permissions.IsAuthenticated,
	]



class UserSearch(generics.ListAPIView):
	serializer_class = SoftUserSerializer

	permission_classes = [
		permissions.IsAuthenticated,
	]

	def get_queryset(self):
		q = self.request.query_params.get('q').strip() or ""
		return User.objects.filter(last_name__icontains=q)[:5]