from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Sale)
admin.site.register(SaleItem)
admin.site.register(Offer)
