# accounts.admin.py
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from user_app.forms import UserAdminCreationForm, UserAdminChangeForm
from news_app.models import Tweet

User = get_user_model()

class TweetHistoryInline(admin.StackedInline):
    model = Tweet.related_users.through
    extra = 0


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('username', 'email', '_is_superuser')
    list_filter = ('_is_superuser',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('last_name', 'first_name')}),
        ('Permissions', {'fields': ('_is_superuser', '_is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'last_name', 'first_name', 'password1', 'password2')}
        ),
    )
    search_fields = ('username', 'email', 'last_name', 'first_name')
    ordering = ('username',)
    filter_horizontal = ()

    inlines = [
        TweetHistoryInline,
    ]


admin.site.register(User, UserAdmin)

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)