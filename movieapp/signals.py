from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile
from django.utils import timezone
from django.contrib.auth.signals import user_logged_in


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, *args, **kwargs):
    instance.profile.save()


@receiver(user_logged_in)
def update_last_login(sender, user, request, **kwargs):
    user.user_last_login = timezone.now()
    user.save(update_fields=["last_login"])
