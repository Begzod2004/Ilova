from django.db import models
from .enums import UserRoles
from django.contrib.auth.models import BaseUserManager
from django.contrib import auth
from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone, password, email=None, **extra_fields):
        if email:
            email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        user = self.model(
            phone=phone,
            password=password,
            email=email,
            **extra_fields
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        if phone is None:
            raise TypeError('User should have a phone_number')
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")

        return self.create_user(phone, password, **extra_fields)


class DirectorsManager(CustomUserManager):
    def get_queryset(self):
        return super(DirectorsManager, self).get_queryset().filter(
            role=UserRoles.director.value)

    def create(self, **kwargs):
        kwargs.update({'role': UserRoles.director.value})
        return super(DirectorsManager, self).create(**kwargs)



class SimpleUserManager(CustomUserManager):
    def get_queryset(self):
        return super(SimpleUserManager, self).get_queryset().filter(
            role=UserRoles.simpleuser.value)


class StaffManager(CustomUserManager):
    def get_queryset(self):
        return super(StaffManager, self).get_queryset().filter(
            role__in=(UserRoles.director.value, UserRoles.manager.value))
