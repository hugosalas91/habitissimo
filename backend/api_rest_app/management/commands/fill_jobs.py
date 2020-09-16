#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from api_rest_app.models import Job
from django.utils import timezone


class Command(BaseCommand):
    """
    Command responsible for filling the Job table.
    """
    help = 'Command responsible for filling the Job table.'

    def handle(self, *args, **options):
        list_of_jobs = [
            "Pintores", "Pintar Interior De Vivienda", "Quitar o Poner Gotelé", "Otros Trabajos De Pintura", "Pintar Exterior Casa (Unifamiliar)", "Lacar Puertas", "Pintar Exterior Vivienda", "Pintar Interior De Local", "Lacar Muebles", "Quitar Papel o Empapelar", "Pintar Interior Edificio", "Pintar Exterior Edificio", "Pintar Exterior Local", "Fontaneros", "Otros Trabajos De Fontanería", "Desatascar Tuberías", "Hacer Instalación Completa Fontanería", "Boletines Instalaciones Agua", "Cambiar Fontanería Cocina o Baño", "Reformar Instalación Fontanería", "Reparar bajantes", "Instalar Grifo Con Sensor O Con Pedal"
        ]
        
        for j in list_of_jobs:
            obj, created = Job.objects.get_or_create(
                name=j, 
                defaults={
                    "updated": timezone.now()
                }
            )
            
            if not created:
                obj.updated = timezone.now()
                obj.save()