from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core.validators import RegexValidator
from django.db import models

from persistence.enums import UserType
from persistence.managers.user_manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, unique=True,
                                    validators=[RegexValidator(regex='^\d{11}$',
                                                               message='Phone number must consist of 11 numbers',
                                                               code='nomatch')
                                                ])
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    type = models.CharField(max_length=20, choices=UserType.choices(), default="PT")

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    ordering = ('email',)

    objects = CustomUserManager()

    @property
    def is_staff(self):
        return self.is_admin

    def update(self, fields_dict):
        password = fields_dict.pop("password")
        if password:
            self.set_password(password)
        for key, value in fields_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
        return self
