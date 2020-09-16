#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.utils import timezone


class Command(BaseCommand):
    """
    Command responsible for creating the anonymous user.
    """
    help = 'Command responsible for creating the anonymous user.'

    def handle(self, *args, **options):
        try:
            token = Token.objects.get(key="db8b6ac7db6f80a10078b4bt0192e79ea1f679c1")
        except Token.DoesNotExist:
            user = User.objects.create(
                password="",
                last_login=timezone.now(),
                is_superuser=False,
                username="default",
                first_name="default",
                last_name="default", 
                email="default@default.es", 
                is_staff=False,
                is_active=True,
                date_joined=timezone.now()
            )
            
            token = Token.objects.create(
                key="db8b6ac7db6f80a10078b4bt0192e79ea1f679c1", 
                user_id=user.pk,
                created=timezone.now()
            )
            