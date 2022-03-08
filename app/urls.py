from django.urls import path

from app.views import index, store_detail


urlpatterns = [
    path('', index),
    path('store/<store_link>/<id>', store_detail, name="store_detail")
]