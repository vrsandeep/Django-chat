from django.contrib import admin
from .models import Chat


class ChatAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'content')
    list_filter = ('room',)


admin.site.register(Chat, ChatAdmin)
