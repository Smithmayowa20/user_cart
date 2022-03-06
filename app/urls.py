from django.urls import path

from app.views import index, store_detail


urlpatterns = [
    path('', index),
    path('store/<store_link>/', store_detail, name="store_detail")
]