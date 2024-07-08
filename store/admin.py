from django.contrib import admin
from .models import *
# Register models so they appear on the built-in SQlite db

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
