from django.contrib import admin
from .models import *

class itemAdmin(admin.ModelAdmin):
    list_display = ('name','get_category_name')

    def get_category_name(self, obj):
        return getattr(obj.category, 'category_name', '')

    get_category_name.short_description = 'category:'

admin.site.register(User_Registration)
admin.site.register(category)
admin.site.register(item)
admin.site.register(bannerads)
admin.site.register(offer_zone)
admin.site.register(Profile_User)
admin.site.register(checkout_item)
admin.site.register(checkout)
