from django.contrib import admin
from .models import Chat


class ChatAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'content')
    filter_fields = ('room')


admin.site.register(Chat, ChatAdmin)
