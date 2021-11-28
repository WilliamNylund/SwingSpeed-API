from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

def user_directory_path(instance, filename):
# file will be uploaded to MEDIA_ROOT/profile-picture/user_<id>/<filename>
    return 'profile-pictures/user_{0}/{1}'.format(instance.id, filename)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), unique=True, max_length=20, blank=False)
    email = models.EmailField(_('email address'), unique=True, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)
    profile_picture = models.ImageField(upload_to=user_directory_path, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username
