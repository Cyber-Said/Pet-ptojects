from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, nickname, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(nickname=nickname, email=email, **extra_fields)  # Передаем дополнительные поля через **extra_fields
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(nickname, email, password, **extra_fields)
class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'nickname'  # Это будет полем для аутентификации
    REQUIRED_FIELDS = ['email']  # Обязательно для superuser

    def has_perm(self, perm, obj=None):
        return self.is_superuser or self.has_module_perms(perm)

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_user_permissions(self):

        return []

    def get_group_permissions(self):
        return []