from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group


class FoodgramUserManager(BaseUserManager):
    """Ensure all required fields for programmatic objects creation"""
    def create_user(self, username, first_name, last_name,
                    email, password, **extra_fields):
        if not username:
            raise ValueError('username must be set')
        if not email:
            raise ValueError('email must be set')
        if not first_name:
            raise ValueError('first_name must be set')
        if not last_name:
            raise ValueError('last_name must be set')
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields)
        if extra_fields.get('is_staff'):
            user.groups.add(Group.objects.get(name='admin'))
        user.set_password(password)
        user.save()
        return user

    def create(self, **kwargs):
        self.create_user(**kwargs)

    def create_superuser(self, username, first_name, last_name, 
                         email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            **extra_fields)