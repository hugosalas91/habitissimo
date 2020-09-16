#-*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from api_rest_app.models import Category, Backpack, Bag, Item, ItemsBackpack
from django.utils import timezone


class Command(BaseCommand):
    """
    Command responsible for initialize example of backpack.
    """
    help = 'Command responsible for initialize example of backpack.'

    def handle(self, *args, **options):
        # Get Backpack
        backpack = Backpack.objects.get(name="Backpack")
        
        # Create metal bag
        metal_category = Category.objects.get(name="Metals")
        
        obj, created = Bag.objects.get_or_create(
            name="Bag with metals 1", 
            defaults={
                "category": metal_category, 
                "max_number_of_items": 4, 
                "order": 1,
                "updated": timezone.now()
            }
        )

        if not created:
            obj.updated = timezone.now()
            obj.save()
            
        # Create items in backpack
        list_of_items = ['Leather', 'Iron', 'Copper', 'Marigold', 'Wool', 'Gold', 'Silk', 'Copper']
        
        for i in list_of_items:
            new_order = 1
            last_item_backpack = ItemsBackpack.objects.all().last()
            if last_item_backpack:
                new_order = last_item_backpack.order + 1
            item = Item.objects.get(name=i)
            i = ItemsBackpack.objects.create(
                backpack=backpack, 
                item=item, 
                order=new_order
            )
            