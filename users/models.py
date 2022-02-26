from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from .managers import UserManager

def user_directory_path(instance, filename):
# file will be uploaded to MEDIA_ROOT/profile-picture/user_<id>/<filename>
    return 'profile-pictures/user_{0}/{1}'.format(instance.id, filename)

class User(AbstractBaseUser, PermissionsMixin):
    class Gender(models.IntegerChoices):
        MALE = 0
        FEMALE = 1
        OTHER = 2
    
    username = models.CharField(_('username'), unique=True, max_length=20, blank=False)
    email = models.EmailField(_('email address'), unique=True, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)
    profile_picture = models.ImageField(upload_to=user_directory_path, blank=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(150)])
    gender = models.IntegerField(choices=Gender.choices, null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    handicap = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(36)])
    lefty = models.BooleanField(null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    
