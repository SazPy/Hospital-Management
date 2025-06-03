from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    for name in ("ADMIN", "DOCTOR", "PATIENT"):
        Group.objects.get_or_create(name=name)
