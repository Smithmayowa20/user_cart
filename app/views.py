from django.shortcuts import render

# Create your views here.
from django.core.paginator import Paginator

from django.http import HttpResponse

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


def store_detail(request,store_link):
    
    store_collections = requests.get("https://www.{store_link}/collections.json?limit=250&page=0".format(store_link=store_link)).json()
    store_products =  requests.get("https://www.{store_link}/products.json?limit=250&page=0".format(store_link=store_link)).json()

    print(store_products['products'][0]['images'])
    context = {'store_products': store_products['products'], 'store_collections':store_collections['collections'], 'store_link':store_link}
    # sending the page object to index.html
    return render(request, 'store_detail.html', context)
