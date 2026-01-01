from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Employee


@receiver(post_save, sender=User)
def create_employee_for_superuser(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        Employee.objects.create(
            user=instance,
            first_name=instance.first_name or "Admin",
            last_name=instance.last_name or "",
            official_email=instance.email,
            title="CEO",
        )
