from django.contrib import admin

from . import models


class MiwoUserAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.MiwoUser, MiwoUserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Profile, ProfileAdmin)


class CampaignAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Campaign, CampaignAdmin)


class ProductAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Product, ProductAdmin)


class ProductImageAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.ProductImage, ProductImageAdmin)
