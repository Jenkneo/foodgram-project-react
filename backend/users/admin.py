from django.contrib import admin

from .models import MyUser, Subscriptions, Favorites, Carts

admin.site.register(MyUser)
admin.site.register(Subscriptions)
admin.site.register(Favorites)
admin.site.register(Carts)
