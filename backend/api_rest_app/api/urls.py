from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^jobs/', views.get_jobs), 
    url(r'^backpack/', views.get_backpack), 
    url(r'^bags/', views.get_bags), 
    url(r'^categories/', views.get_categories),
    url(r'^items/', views.get_items), 
    url(r'^create-bag/', views.create_bag), 
    url(r'^insert-item/', views.insert_item), 
    url(r'^clean-all/', views.clean_all), 
    url(r'^ordenate-bags/', views.ordenate_bags),
]