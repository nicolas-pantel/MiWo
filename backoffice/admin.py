from django.contrib import admin

from . import models


class ProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Profile, ProfileAdmin)


class CampaignAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Campaign, CampaignAdmin)
