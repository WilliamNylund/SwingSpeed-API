from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from users.models import User
from django.conf import settings
from django.contrib.auth import get_user_model

def user_directory_path(instance, filename):
# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'recordings/user_{0}/{1}'.format(instance.user.id, filename)

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Swing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user)) #default get current user
    speed = models.FloatField(null=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    is_active = models.BooleanField(default=True, null=False)
    note = models.TextField(blank=True, null=False)
    recording = models.FileField(upload_to=user_directory_path, blank=True)

    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return self.user.username + ': ' + str(self.speed)
