from django.contrib import admin
from .models import Job, Category, Backpack, Bag, Item


class JobAdmin(admin.ModelAdmin):
    list_display = ["name", "active", "created", "updated"]
    
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "active", "created", "updated"]
    

class ItemInline(admin.TabularInline):
    model = Backpack.backpack_items.through
    extra = 1
    

class BackpackAdmin(admin.ModelAdmin):
    list_display = ["name", "max_number_of_items", "active", "created", "updated"]
    inlines = [ItemInline]
    
    
class BagAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "max_number_of_items", "order", "active", "created", "updated"]
    inlines = [ItemInline]
    
    
class ItemAdmin(admin.ModelAdmin):
    list_display = ["category", "name", "active", "created", "updated"]
    
    
admin.site.register(Job, JobAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Backpack, BackpackAdmin)
admin.site.register(Bag, BagAdmin)
admin.site.register(Item, ItemAdmin)
