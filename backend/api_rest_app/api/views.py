# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api_rest_project.utils import response_dictionary
from rest_framework import status
from api_rest_app.models import Job, Category, Backpack, Bag, Item, ItemsBackpack
from .serializers import JobSerializer, BackpackSerializer, BagSerializer, CategorySerializer, ItemSerializer
from django.utils import timezone


@api_view(['GET'])
def get_jobs(request):
    """
    Filtrado de los trabajos
    ---
    parameters:
        - name: name
          description: Contenido del trabajo a buscar
          required: true
          type: string
          paramType: query

    responseMessages:
        - code: 200
          message: Devolución de los datos
        - code: 400
          message: Se ha producido algún problema con los datos
    """
    search = request.GET.get('search', None)
    
    if not search:
        data = response_dictionary(0, _(u'No se ha enviado el parámetro de búsqueda'), {})
        return Response(data, status=status.HTTP_400_BAD_REQUEST)    
    
    jobs = Job.objects.filter(
        name__icontains=search, 
        active=True
    ).order_by("name")

    serializer = JobSerializer(jobs, many=True).data
    data = response_dictionary(1, '', serializer)
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_backpack(request):
    """
    Retorna los datos y el contenido de la mochila
    ---
    responseMessages:
        - code: 200
          message: Devolución de los datos
        - code: 400
          message: Se ha producido algún problema con los datos
    """
    try:
        backpack = Backpack.objects.get(
            name="Backpack", 
            active=True
        )
    except Backpack.DoesNotExist:
        data = response_dictionary(0, _(u'No se ha enviado el parámetro de búsqueda'), {})
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    except Backpack.MultipleObjectsReturned:
        data = response_dictionary(0, _(u'No se ha enviado el parámetro de búsqueda'), {})
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
    serializer = BackpackSerializer(backpack).data
    data = response_dictionary(1, '', serializer)
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_bags(request):
    """
    Retorna los datos y el contenido de las bolsas
    ---
    responseMessages:
        - code: 200
          message: Devolución de los datos
        - code: 400
          message: Se ha producido algún problema con los datos
    """
    bags = Bag.objects.filter( 
        active=True
    ).order_by("order")
        
    serializer = BagSerializer(bags, many=True).data
    data = response_dictionary(1, '', serializer)
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_categories(request):
    """
    Retorna los datos y el contenido de las categorias
    ---
    responseMessages:
        - code: 200
          message: Devolución de los datos
        - code: 400
          message: Se ha producido algún problema con los datos
    """
    categories = Category.objects.filter( 
        active=True
    ).order_by("name")
        
    serializer = CategorySerializer(categories, many=True).data
    data = response_dictionary(1, '', serializer)
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_items(request):
    """
    Retorna los datos y el contenido de los items
    ---
    responseMessages:
        - code: 200
          message: Devolución de los datos
        - code: 400
          message: Se ha producido algún problema con los datos
    """
    items = Item.objects.filter( 
        active=True
    ).order_by("name")
        
    serializer = ItemSerializer(items, many=True).data
    data = response_dictionary(1, '', serializer)
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_bag(request):
    """
    Crea una nueva bolsa y retorna los datos y el contenido de todas las bolsas y la mochila.
    ---
    responseMessages:
        - code: 200
          message: Devolución de los datos
        - code: 400
          message: Se ha producido algún problema con los datos
    """
    name = request.data.get("name", None)
    category = request.data.get("category", None)
    if name:
        try:
            bag_exists = Bag.objects.get(name=name)
            data = response_dictionary(0, _(u'Ya existe una bolsa con ese nombre.'), {})
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Bag.DoesNotExist:
            pass
        
        category_obj = None
        if category:
            try:
                category_obj = Category.objects.get(id=int(category))
            except Category.DoesNotExist:
                pass
            
        new_order = 1
        bags = Bag.objects.all()
        if bags.count() >= 4:
            data = response_dictionary(0, _(u'Sólo se puede crear un máximo de 4 bolsas extra.'), {})
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        ordered_bags = bags.order_by("-order")
        if ordered_bags:
            new_order = ordered_bags[0].order + 1
        
        new_bag = Bag.objects.create(
            name=name, 
            category=category_obj, 
            max_number_of_items=4, 
            order=new_order,
            updated=timezone.now()
        )
    
    backpack = None
    try:
        backpack = Backpack.objects.get(
            name="Backpack", 
            active=True
        )
    except Backpack.DoesNotExist:
        data = response_dictionary(0, _(u'No se ha enviado el parámetro de búsqueda'), {})
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    except Backpack.MultipleObjectsReturned:
        data = response_dictionary(0, _(u'No se ha enviado el parámetro de búsqueda'), {})
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    bags = Bag.objects.filter( 
        active=True
    ).order_by("order")
    
    serializer = {
        'backpack': BackpackSerializer(backpack).data,
        'bags': BagSerializer(bags, many=True).data
    }

    data = response_dictionary(1, '', serializer)
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def insert_item(request):
    """
    Crea un nuevo item y lo añade en la mochila o en una bolsa.
    ---
    responseMessages:
        - code: 200
          message: Devolución de los datos
        - code: 400
          message: Se ha producido algún problema con los datos
    """
    item_id = request.data.get("item_id", None)
    if item_id:
        item = None
        try:
            item = Item.objects.get(id=int(item_id))
        except Exception:
            data = response_dictionary(0, _(u'Ya existe una bolsa con ese nombre.'), {})
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            backpack = Backpack.objects.get(name="Backpack")
        except Backpack.DoesNotExist:
            data = response_dictionary(0, _(u'Ya existe una bolsa con ese nombre.'), {})
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        last_item_backpack = ItemsBackpack.objects.all().last()
        new_order = 1
        if last_item_backpack:
                new_order = last_item_backpack.order + 1
                
        items_in_backpack = backpack.backpack_items.all().count()
        
        if items_in_backpack < 8:
            i = ItemsBackpack.objects.create(
                backpack=backpack, 
                item=item, 
                order=new_order
            )
        else:
            bags = Bag.objects.filter(active=True).order_by("order")
            for b in bags:
                items_in_bag = b.backpack_items.all().count()
                if items_in_bag < 4:
                    i = ItemsBackpack.objects.create(
                        backpack=b, 
                        item=item, 
                        order=new_order
                    )
                    break
    
    backpack = None
    try:
        backpack = Backpack.objects.get(
            name="Backpack", 
            active=True
        )
    except Backpack.DoesNotExist:
        data = response_dictionary(0, _(u'No existe la mochila'), {})
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    except Backpack.MultipleObjectsReturned:
        data = response_dictionary(0, _(u'Existen varias mochilas'), {})
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    bags = Bag.objects.filter( 
        active=True
    ).order_by("order")
    
    serializer = {
        'backpack': BackpackSerializer(backpack).data,
        'bags': BagSerializer(bags, many=True).data
    }

    data = response_dictionary(1, '', serializer)
    return Response(data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def clean_all(request):
    """
    Limpia las tablas del problema de la mochila.
    ---
    responseMessages:
        - code: 200
          message: Devolución de los datos
        - code: 400
          message: Se ha producido algún problema con los datos
    """
    
    ItemsBackpack.objects.all().delete()
    Bag.objects.all().delete()
    
    serializer = {}

    data = response_dictionary(1, '', serializer)
    return Response(data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def ordenate_bags(request):
    """
    Ordena los items en las bolsas.
    ---
    responseMessages:
        - code: 200
          message: Devolución de los datos
        - code: 400
          message: Se ha producido algún problema con los datos
    """
    backpack = None
    try:
        backpack = Backpack.objects.get(
            name="Backpack", 
            active=True
        )
    except Backpack.DoesNotExist:
        data = response_dictionary(0, _(u'No existe la mochila'), {})
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    except Backpack.MultipleObjectsReturned:
        data = response_dictionary(0, _(u'Existen varias mochilas'), {})
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    # we put all the items in the backpack
    all_items = ItemsBackpack.objects.all()
    all_items.update(backpack=backpack)
    
    categories = Category.objects.filter(active=True)
    
    for c in categories:
        # We see what bags there are for each category
        bags_in_category = Bag.objects.filter(
            active=True,
            category=c
        )
        
        if bags_in_category:
            number_of_bags = bags_in_category.count()
            max_number_of_items = number_of_bags * bags_in_category[0].max_number_of_items
            
            # we sort the items in that category in alphabetical order
            items_in_bags = ItemsBackpack.objects.filter(item__category=c)
            number_of_items_in_bags = items_in_bags.count()
            
            # we are left only with the items that fit in the backpacks that are in that category
            items_for_bags = items_in_bags.order_by("item__name")[:max_number_of_items]
                
            # We are putting the items in the bags of their category and changing the value of the order field so that they go in alphabetical order
            bag = 0
            cont_bag = 0
            for count, i in enumerate(items_for_bags):
                i.order = count + 1
                i.backpack = bags_in_category[bag]
                i.save()
                
                cont_bag += 1
                if cont_bag == bags_in_category[0].max_number_of_items:
                    bag += 1
                    cont_bag = 0
                    
    # We see what items are left in the backpack and we order them
    items_in_backpack = ItemsBackpack.objects.filter(backpack=backpack)
    items_in_backpack = items_in_backpack.order_by("item__name")
    for cont, i in enumerate(items_in_backpack):
        i.order = cont + 1
        i.save()
    
    # We leave the 8 items in the backpack and the rest we are putting in the holes in the backpacks
    if items_in_backpack:
        rest_of_items = items_in_backpack[backpack.max_number_of_items:]
        bags = Bag.objects.all().order_by('order')
        for b in bags:
            items_in_bag = b.backpack_items.all().count()
            free_spaces = b.max_number_of_items - items_in_bag
            for f in range(free_spaces):
                try:
                    rest_of_items[f].backpack = b
                    rest_of_items[f].save()
                except Exception:
                    break
            if len(rest_of_items) > free_spaces:
                rest_of_items = rest_of_items[free_spaces:]
            
            items_in_bag_ordered = ItemsBackpack.objects.filter(backpack=b)
            items_in_bag_ordered = items_in_bag_ordered.order_by("item__name")
            for cont, i in enumerate(items_in_bag_ordered):
                i.order = cont + 1
                i.save()
            
    bags = Bag.objects.filter( 
        active=True
    ).order_by("order")
    
    serializer = {
        'backpack': BackpackSerializer(backpack).data,
        'bags': BagSerializer(bags, many=True).data
    }

    data = response_dictionary(1, '', serializer)
    return Response(data, status=status.HTTP_200_OK)
