from django.shortcuts import render

# Create your views here.
from django.core.paginator import Paginator

from django.http import HttpResponse

from decimal import Decimal

import csv

import requests

file = "app/Top 10,000 Shopify Stores Dataset - October 2020.csv"

with open(file, newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

def index(request):
    p = Paginator(data[1:], 100)
    # getting the desired page number from url
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    context = {'page_obj': page_obj}
    # sending the page object to index.html
    return render(request, 'index.html', context)


def store_detail(request,store_link,id):
    i = 0
    store_collections = []
    store_products = requests.get("https://www.{store_link}/products.json?limit=250&page={id}".format(store_link=store_link,id=id)).json()['products']
    
    while 1:
        collections = requests.get("https://www.{store_link}/collections.json?limit=250&page={page_number}".format(store_link=store_link,page_number=i)).json()['collections']
        if len(collections):
            store_collections += collections
            i += 1
        else:
            break

    total_stock = sum([collection['products_count'] for collection in store_collections])
    total_vendors = list(set([product['vendor'] for product in store_products]))
    prices = [Decimal(product['variants'][0]['price']) for product in store_products]

    has_next = True if requests.get("https://www.{store_link}/products.json?limit=250&page={id}".format(store_link=store_link,id=int(id)+1)).json()['products'] else False
    next_id = int(id) + 1
    has_previous = True if int(id) else False
    previous_id = int(id) - 1
    context = {
        'store_products': store_products, 'has_next':has_next, 'has_previous':has_previous,
        'next_id': next_id, 'previous_id':previous_id, 'id':id, 'total_number_of_collections': len(store_collections),
        'total_vendors': len(total_vendors), 'average_price': sum(prices)/len(prices), 'highest_price': max(prices),
        'lowest_price':min(prices),
        'total_stock':total_stock, 'store_collections':store_collections, 'store_link':store_link
    }
    # sending the page object to index.html
    return render(request, 'store_detail.html', context)
