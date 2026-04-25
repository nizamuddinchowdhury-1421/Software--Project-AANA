from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True, help_text='Upload your profile photo')
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text='Your contact number')
    address = models.TextField(blank=True, null=True, help_text='Your address')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url') and self.photo.url:
            return self.photo.url
        return '/static/img/default-avatar.svg'
    
    def get_display_name(self):

        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.get_username()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:

        if not hasattr(instance, 'profile'):
            UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):

    if hasattr(instance, 'profile') and not kwargs.get('created', False):
        instance.profile.save()
