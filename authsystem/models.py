from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **other_fields):
        if username is None:
            raise TypeError('User must have a username')
        
        if email is None:
            raise TypeError('User must have an email address')
        
        user = self.model(username=username, email=self.normalize_email(email))
        for field, value in other_fields.items():
            if hasattr(user, field):
                setattr(user, field, value)
        
        user.set_password(password)
        user.set_password(password)
        user.save()
        
        return user
    
    def create_superuser(self, email, username='admin', password=None):
        if password is None:
            raise TypeError('Superuser must have a password')
        
        user = self.create_user(username=username, email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True, db_index=True)
    username = models.CharField(db_index=True, max_length=255, blank=False, unique=True, verbose_name='Username')
    email = models.EmailField(db_index=True, unique=True, blank=False, max_length=100, verbose_name='Email')
    avatar = models.ImageField(blank=True, upload_to='user/avatar', verbose_name='Avatar')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Create time')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Update time')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    objects = UserManager()
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def __str__(self):
        return self.email
    