from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


ROOMS = (
    ('public', 'public'),
    ('room1', 'room1'),
    ('room2', 'room2')
)


class Chat(models.Model):

    # room be moved into a model, and following key becomes FK
    room = models.CharField(choices = ROOMS, max_length=64, default=ROOMS[0][0])
    content = models.CharField(max_length=255, null=False, blank=False)
    user = models.ForeignKey(User, null=False)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    def __unicode__(self):
        return u'%s : %s' % (self.room, self.user.username)
