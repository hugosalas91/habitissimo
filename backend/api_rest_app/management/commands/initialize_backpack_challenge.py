#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from api_rest_app.models import Category, Backpack, Bag, Item
from django.utils import timezone


class Command(BaseCommand):
    """
    Command responsible for initialize backpack challenge.
    """
    help = 'Command responsible for initialize backpack challenge.'

    def handle(self, *args, **options):
        # Create categories
        list_of_categories = [
            'Clothes', 'Metals', 'Weapons', 'Herbs'
        ]
        
        for c in list_of_categories:
            obj, created = Category.objects.get_or_create(
                name=c, 
                defaults={
                    "updated": timezone.now()
                }
            )
            
            if not created:
                obj.updated = timezone.now()
                obj.save()
                
        # Create backpack
        obj, created = Backpack.objects.get_or_create(
            name="Backpack", 
            defaults={
                "max_number_of_items": 8, 
                "updated": timezone.now()
            }
        )

        if not created:
            obj.updated = timezone.now()
            obj.save()
            
        # Create Items
        dict_of_items = {
            "Leather": "Clothes", 
            "Linen": "Clothes", 
            "Silk": "Clothes", 
            "Wool": "Clothes", 
            "Copper": "Metals", 
            "Gold": "Metals", 
            "Iron": "Metals", 
            "Silver": "Metals", 
            "Axe": "Weapons", 
            "Dagger": "Weapons", 
            "Mace": "Weapons", 
            "Sword": "Weapons", 
            "Cherry Blossom": "Herbs", 
            "Marigold": "Herbs", 
            "Rose": "Herbs", 
            "Seaweed": "Herbs"
        }
        
        for key, value in dict_of_items.items():
            category = Category.objects.get(name=value)
            
            obj, created = Item.objects.get_or_create(
                name=key, 
                defaults={
                    "category": category, 
                    "updated": timezone.now()
                }
            )

            if not created:
                obj.updated = timezone.now()
                obj.save()
            