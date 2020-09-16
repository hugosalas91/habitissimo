# -*- coding: utf-8 -*-
from rest_framework import serializers
from api_rest_app.models import Job, Category, Backpack, Bag, Item


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = ('id', 'name',)
        
        
class BackpackSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField('_get_items')

    class Meta:
        model = Backpack
        fields = ('id', 'name', 'max_number_of_items', 'items')
        
    def _get_items(self, obj):
        if obj:
            return obj.items
        return ''
    
    
class ItemSerializer(serializers.ModelSerializer):
    category_id = serializers.SerializerMethodField('_get_category_id')
    category_name = serializers.SerializerMethodField('_get_category_name')

    class Meta:
        model = Item
        fields = ('id', 'category_id', 'category_name', 'name')
        
    def _get_category_id(self, obj):
        if obj and obj.category:
            return obj.category.id
        return ''
    
    def _get_category_name(self, obj):
        if obj and obj.category:
            return obj.category.name
        return ''
    
    
class BagSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField('_get_items')
    category_id = serializers.SerializerMethodField('_get_category_id')
    category_name = serializers.SerializerMethodField('_get_category_name')

    class Meta:
        model = Bag
        fields = ('id', 'name', 'max_number_of_items', 'items', 'category_id', 'category_name', 'order')
        
    def _get_items(self, obj):
        if obj:
            return obj.items
        return ''
    
    def _get_category_id(self, obj):
        if obj and obj.category:
            return obj.category.id
        return ''
    
    def _get_category_name(self, obj):
        if obj and obj.category:
            return obj.category.name
        return ''
    
    
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')
