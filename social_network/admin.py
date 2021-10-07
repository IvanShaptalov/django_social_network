from django.contrib import admin

# Register your models here.
from social_network.models import PostUser, Post
from social_network.utilities import send_activation_notification


def send_activation_notifications(model_admin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    model_admin.message_user(request, 'Mails sent')


send_activation_notifications.short_description = 'Activation mails to users'


class PostUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'last_login', 'date_joined', 'date_last_request')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fields = (('username', 'email'), ('first_name', 'last_name'),
              ('is_active', 'is_activated'),
              ('is_staff', 'is_superuser'), 'groups',
              'user_permissions',
              ('date_joined',))
    readonly_fields = ('last_login', 'date_joined')

    actions = (send_activation_notifications,)


class PostAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'title', 'author', 'like_count', 'unlike_count')
    search_fields = ('title', 'content', 'author')
    fields = (('title', 'content'), ('image',),
              ('is_active',),
              ('author',))
    readonly_fields = ('created_at',)


# solved create all in admin
admin.site.register(PostUser, PostUserAdmin)
admin.site.register(Post, PostAdmin)
