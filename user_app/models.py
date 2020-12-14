from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class UserManager(BaseUserManager):
	def create_user(self, username, email, last_name, first_name, password=None, is_active=True, is_staff=False, is_superuser=False):
		if not username:
			return ValueError('Users must have an username')
		if not email:
			return ValueError('Users must have an email address')
		if not password:
			return ValueError('Users must have a password')
		if not last_name:
			return ValueError('Users must have a last name')
		if not first_name:
			return ValueError('Users must have a first name')

		user_obj = self.model(
			username = username,
			email = self.normalize_email(email),
			last_name = last_name.capitalize(),
			first_name = first_name.capitalize()
		)
		user_obj.set_password(password)

		user_obj._is_active = is_active
		user_obj._is_staff = is_staff
		user_obj._is_superuser = is_superuser

		user_obj.save(using=self._db)
		return user_obj

	def create_staffuser(self, username, email, last_name, first_name, password=None):
		user_obj = self.create_user(
			username, email, last_name, first_name,
			password = password,
			is_staff = True
		)
		return user_obj

	def create_superuser(self, username, email, last_name, first_name, password=None):
		user_obj = self.create_user(
			username, email, last_name, first_name,
			password 			= password,
			is_staff 			= True,
			is_superuser 	= True
		)
		return user_obj

# Constants User related
DEFAULT_USER_PIC_URI = '/static/default_profile_pic.png'

class User(AbstractBaseUser):
	username				= models.CharField(max_length=255, primary_key=True)
	email						= models.EmailField(unique=True)

	last_name				= models.CharField(max_length=255)
	first_name			= models.CharField(max_length=255)

	_is_active			= models.BooleanField(default=True)
	_is_staff				= models.BooleanField(default=False)
	_is_superuser		= models.BooleanField(default=False)

	timestamp				= models.DateTimeField(auto_now_add=True)

	picture					= models.ImageField(upload_to='user_pic/', default=None, null=True)
	follow					= models.ManyToManyField('self', blank=True, symmetrical=False, related_name="follower")

	USERNAME_FIELD	= 'username'
	EMAIL_FIELD			= 'email'
	REQUIRED_FIELDS = ['email', 'last_name', 'first_name']

	objects = UserManager()

	def get_full_name(self):
		return self.last_name + ' ' + self.first_name

	def get_short_name(self):
		return self.first_name

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_active(self):
		return self._is_active
	
	@property
	def is_staff(self):
		return self._is_staff

	@property
	def is_admin(self):
		return self._is_admin

	def toggleFollow(self, following):
		if self.follow.filter(pk=following.pk).exists():
			self.follow.remove(following)
			return False
		else:
			self.follow.add(following)
			return True

	def is_followed(self, current_user):
			return self.follower.filter(pk=current_user.pk).exists()