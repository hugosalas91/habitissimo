import json
from django.shortcuts import render
from .api import ApiClient
from requests.models import Response
from django.http import HttpResponse


# Api connection Object
global apiConnection
apiConnection = ApiClient()


# Error Api Management
def response_message(rs):
    # print rs
    if isinstance(rs, Response):
        return None, None, rs.content, None

    if 'detail' in rs.keys():
        return None, rs.get('detail'), None, True

    if 'error' in rs.keys():
        return rs['error'].get('status', None), rs['error'].get('msg', None), rs['error'].get('results', None), True

    elif 'status' in rs.keys() and rs['status'] == 0:
        return rs.get('status', None), rs.get('msg', None), rs.get('results', None), True

    else:
        return rs.get('status', None), rs.get('msg', None), rs.get('results', None), False


def home(request, tag_slug=None):
    ec = {}
    
    if request.method == "POST":
        search = request.POST.get("search", None)
        if search:
            ec.update({'search': search})
        
    # Backpack data
    url = 'backpack/'
    rs = apiConnection.call('GET', url, {})
    status, msg, results, error = response_message(rs)
    if results:
        ec.update({'backpack': results})
        
    # Bags data
    url = 'bags/'
    rs = apiConnection.call('GET', url, {})
    status, msg, results, error = response_message(rs)
    if results:
        ec.update({'bags': results})
        
    # Categories
    url = 'categories/'
    rs = apiConnection.call('GET', url, {})
    status, msg, results, error = response_message(rs)
    if results:
        ec.update({'categories': results})
        
    # Categories
    url = 'items/'
    rs = apiConnection.call('GET', url, {})
    status, msg, results, error = response_message(rs)
    if results:
        ec.update({'items': results})
        
    return render(request, 'front_app/home.html', ec)


def autocomplete(request):
    str = request.GET.get('str', None)
    
    url = 'jobs/?search=' + str

    rs = apiConnection.call('GET', url, {})
    status, msg, results, error = response_message(rs)

    return HttpResponse(json.dumps(results))


def create_bag(request):
    ec = {}
    
    name = request.GET.get("name", None)
    if name:
        ec.update({"name": name})
        
    category = request.GET.get("category", None)
    if category:
        ec.update({"category": category})
    
    url = 'create-bag/'
    
    rs = apiConnection.call('POST', url, ec)
    status, msg, results, error = response_message(rs)
    if not error:
        results = json.dumps(results)
        return HttpResponse(results)

    return HttpResponse(False)


def insert_item(request):
    ec = {}
    
    item_id = request.GET.get("item_id", None)
    if item_id:
        ec.update({"item_id": item_id})
    
    url = 'insert-item/'
    
    rs = apiConnection.call('POST', url, ec)
    status, msg, results, error = response_message(rs)
    if not error:
        results = json.dumps(results)
        return HttpResponse(results)

    return HttpResponse(False)


def clean_all(request):
    ec = {}
    
    url = 'clean-all/'
    
    rs = apiConnection.call('PUT', url, ec)
    status, msg, results, error = response_message(rs)

    return HttpResponse(False)


def ordenate_bags(request):
    ec = {}
    
    url = 'ordenate-bags/'
    
    rs = apiConnection.call('PUT', url, ec)
    status, msg, results, error = response_message(rs)
    if not error:
        results = json.dumps(results)
        return HttpResponse(results)

    return HttpResponse(False)
