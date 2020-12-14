from django.contrib import admin
from news_app import models

# Register your models here.
class CommentInline(admin.StackedInline):
	model = models.Comment
	extra = 0

class Tweet(admin.ModelAdmin):
	inlines = [
		CommentInline,
	]

admin.site.register(models.Tweet, Tweet)