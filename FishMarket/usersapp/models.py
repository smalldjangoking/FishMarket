from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Користувач повинен мати адресу електронної пошти')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True, verbose_name='Електронна пошта')
    name = models.CharField(max_length=25, null=True, blank=True, verbose_name="Ім'я")
    last_name = models.CharField(max_length=25, null=True, blank=True, verbose_name='Прізвище')
    discount = models.DecimalField(max_digits=4, decimal_places=2, null=True, default=0, verbose_name='Знижка (%)')
    is_staff = models.BooleanField(default=False, verbose_name='Співробітник')
    is_superuser = models.BooleanField(default=False, verbose_name='Власник')
    is_active = models.BooleanField(default=True, verbose_name='Активний')
    last_login = models.DateTimeField(null=True, blank=True, verbose_name='Останній вхід')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата реєстрації')
    is_email_confirmed = models.BooleanField(default=False, verbose_name='Підтверджено електронну пошту')
    phone_number = models.CharField(validators=[MinLengthValidator(8)], max_length=18, null=True, blank=True, verbose_name='Номер телефону')


    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'
