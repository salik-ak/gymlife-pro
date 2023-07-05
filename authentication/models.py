from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from trainer.models import Trainer


# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email,phone, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email,phone, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=20,unique=True,verbose_name='users',
                             blank=False,help_text='enter validusername')
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=20,unique=True,verbose_name='phone number',
                             blank=False,help_text='enter 10 digit phone number')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']
    

    objects = CustomUserManager()


class Notification(models.Model):
    user = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    



@receiver(post_save, sender=User)
def create_user_notification(sender, instance, created, **kwargs):
    if created:
        message = f"A new trainer has been registerd with the username: {instance.username}"
        admin_user = User.objects.get(username='admin')  # Replace 'admin' with the admin username
        notification = Notification(user=admin_user, message=message)
        notification.save()
