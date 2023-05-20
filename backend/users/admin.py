from django.contrib import admin

from .models import MyUser, Subscriptions, Favorites, Carts


@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
         'id', 'username', 'email', 'first_name', 'last_name',
    )
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'


admin.site.register(Subscriptions)
admin.site.register(Favorites)
admin.site.register(Carts)
