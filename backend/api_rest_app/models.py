# -*- coding: utf-8 -*-
from django.db import models


class Job(models.Model):
    name = models.CharField(u'Trabajo', max_length=500, null=True, blank=True)
    active = models.BooleanField(u'Activo', default=True)
    created = models.DateTimeField(u'Fecha de creación', auto_now_add=True)
    updated = models.DateTimeField(u'Fecha de actualización', auto_now=True)
    
    class Meta:
        verbose_name = u'Trabajo'
        verbose_name_plural = u'Trabajos'
        
    def __str__(self):
        return self.name

        
###############################################################        
#                                                             #
#               BACKEND CHALLENGE (BACKPACK)                  #
#                                                             #
############################################################### 

class Category(models.Model):
    name = models.CharField(u'Nombre', max_length=250, null=True, blank=True)
    active = models.BooleanField(u'Activo', default=True)
    created = models.DateTimeField(u'Fecha de creación', auto_now_add=True)
    updated = models.DateTimeField(u'Fecha de actualización', auto_now=True)
    
    class Meta:
        verbose_name = u'Categoría'
        verbose_name_plural = u'Categorías'
        
    def __str__(self):
        return self.name

        
class Backpack(models.Model):
    name = models.CharField(u'Nombre', max_length=250, null=True, blank=True)
    max_number_of_items = models.IntegerField(u'Máximo número de items', blank=True, null=True, default=0)
    active = models.BooleanField(u'Activo', default=True)
    created = models.DateTimeField(u'Fecha de creación', auto_now_add=True)
    updated = models.DateTimeField(u'Fecha de actualización', auto_now=True)
    
    class Meta:
        verbose_name = u'Mochila'
        verbose_name_plural = u'Mochilas'
        
    def __str__(self):
        return self.name
        
    @property
    def items(self):
        from api_rest_app.api.serializers import ItemSerializer
        #items = self.backpack_items.all()
        items = ItemsBackpack.objects.filter(backpack=self).order_by("order").values_list("item_id", flat=True)
        objects = Item.objects.filter(id__in=items)
        objects = dict([(obj.id, obj) for obj in objects])
        sorted_objects = [objects[id] for id in items]
        return ItemSerializer(sorted_objects, many=True).data
        
        
class Bag(Backpack):
    category = models.ForeignKey(Category, verbose_name=u"Categoría", related_name="category_bags", on_delete=models.CASCADE, blank=True, null=True)
    order = models.IntegerField(u'Orden', blank=True, null=True, default=0)
    
    class Meta:
        verbose_name = u'Bolsa'
        verbose_name_plural = u'Bolsas'
        
    def __str__(self):
        return self.name
        
        
class Item(models.Model):
    backpacks = models.ManyToManyField(Backpack, verbose_name=u"Mochila", through='ItemsBackpack', related_name="backpack_items")
    category = models.ForeignKey(Category, verbose_name=u"Categoría", related_name="category_items", on_delete=models.CASCADE)
    name = models.CharField(u'Nombre', max_length=250, null=True, blank=True)
    active = models.BooleanField(u'Activo', default=True)
    created = models.DateTimeField(u'Fecha de creación', auto_now_add=True)
    updated = models.DateTimeField(u'Fecha de actualización', auto_now=True)
                                   
    class Meta:
        verbose_name = u'Item'
        verbose_name_plural = u'Items'
        
    def __str__(self):
        return self.name


class ItemsBackpack(models.Model):
    backpack = models.ForeignKey(Backpack, verbose_name=u"Mochila", related_name="items_in_backpack", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, verbose_name=u"Item", related_name="items_in_backpack", on_delete=models.CASCADE)
    order = models.IntegerField(u'Orden', default=0)
    