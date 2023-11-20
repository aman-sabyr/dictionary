from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.contrib.auth.models import BaseUserManager


class ClientManager(BaseUserManager):

    def _create(self, email, password, **extra_fields):
        # normalize email
        email = self.normalize_email(email)

        # generate activation or recovery code
        activation_code = get_random_string(5)
        extra_fields.update({'activation_code': activation_code})

        # save new user
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        # sends activation code to email
        # self.send_activation_code(email=email, code=activation_code)

        return user

    def create_user(self, email, password, **extra_fields):
        return self._create(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self._create(email, password, **extra_fields)


class Client(AbstractBaseUser):
    nickname = models.CharField(max_length=50, unique=True)
    group = models.CharField(max_length=5)
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=128)
    activation_code = models.CharField(max_length=5)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = ClientManager()

    def __str__(self):
        return f'{self.nickname} from {self.group}'

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff
