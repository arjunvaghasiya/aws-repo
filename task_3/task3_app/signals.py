from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=User)
def create_profile_user(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile.objects.create(user=instance)
        user_profile.save()


@receiver(post_save, sender=Profile)
def create_profile_user(sender, instance, created, **kwargs):
    if created:
        crt_profile = CompanyDetails.objects.create(profile=instance)
        obj1 = User.objects.get(id=crt_profile.id)
        if obj1.is_superuser == True:
            crt_profile.is_hr = True
            crt_profile.is_manager = True
            crt_profile.save()
        else:
            crt_profile.save()
