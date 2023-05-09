from django.contrib import admin
from . models import Category, Product, UserCart

# pokaziavem v admin paneli
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(UserCart)

