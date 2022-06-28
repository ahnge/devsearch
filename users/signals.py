from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print("triggered...")
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name)

        subject = 'Welcome to Devsearch'
        msg = "We are glad you are here!"
        email = EmailMessage(
            subject=subject,
            body=msg,
            from_email=settings.EMAIL_HOST_USER,
            to=[profile.email],
            headers={'Content-Type': 'text/plain'},
        )
        email.send()


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
    user = instance.user
    user.delete()


@receiver(post_save, sender=Profile)
def update_user(sender, instance, created,  **kwargs):
    profile = instance
    user = profile.user
    if not created:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


# post_save.connect(create_profile, sender=User)
# post_delete.connect(delete_user, sender=Profile)
