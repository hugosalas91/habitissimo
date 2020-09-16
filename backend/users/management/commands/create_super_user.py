#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.utils import timezone


class Command(BaseCommand):
    """
    Command responsible for creating the superuser.
    """
    help = 'Command responsible for creating the superuser.'

    def handle(self, *args, **options):
        try:
            token = Token.objects.get(key="502e9129a9676d3d4218cd90159d5246ae882ce2")
        except Token.DoesNotExist:
            user = User.objects.create(
                last_login=timezone.now(),
                is_superuser=True,
                username="habitissimo",
                first_name="Habitissimo",
                last_name="", 
                email="habitissimo@default.es", 
                is_staff=True,
                is_active=True,
                date_joined=timezone.now()
            )
            user.set_password('testpass123')
            user.save()
            
            token = Token.objects.create(
                key="502e9129a9676d3d4218cd90159d5246ae882ce2", 
                user_id=user.pk,
                created=timezone.now()
            )
            