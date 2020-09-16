from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('autocomplete/', views.autocomplete, name="autocomplete"),
    path('create-bag/', views.create_bag, name="create_bag"), 
    path('insert-item/', views.insert_item, name="insert_item"), 
    path('clean-all/', views.clean_all, name="clean_all"), 
    path('ordenate-bags/', views.ordenate_bags, name="ordenate_bags"),
]
