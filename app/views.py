from django.shortcuts import render

# Create your views here.
from datetime import datetime

from django.http import HttpResponse

import csv

file = "app/Top 10,000 Shopify Stores Dataset - October 2020.csv"

with open(file, newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return render(request, 'index.html', {})
