from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment
from django.core.mail import send_mail
#from django.contrib.sites.shortcuts import get_current_site

@receiver(post_save, sender=Comment)
def send_notification_email(sender, instance, created, **kwargs):
    if created:
        subject = f'Your post: "{instance.post.title}" just got a comment'
        content = f'Hi {instance.post.author.username},\n'
        content += f'You just got a comment from {instance.author.username}!\n'
        content += f'Please come back to the site\n'
        #content += f'post/{instance.post.id}/'
        content += f'Regards,\nYour love'

        ToEmail = instance.post.author.email
        send_mail(
            subject,
            content,
            '',
            [ToEmail],
            fail_silently=False,
        )