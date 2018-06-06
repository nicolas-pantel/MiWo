from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models


class InfluencerFollowerListFilter(admin.SimpleListFilter):
    """List filter by Influencer or Follower status"""
    title = _("User status")
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        """Filter display"""
        return (
            ('INFLUENCERS', _('Influencers')),
            ('FOLLOWERS', _("Followers")),
        )

    def queryset(self, request, queryset):
        """Return Influencers or Followers MiwoUsers"""
        if self.value() == 'INFLUENCERS':
            return queryset.filter(campaigns__isnull=False).distinct()
        if self.value() == 'FOLLOWERS':
            return queryset.filter(campaigns__isnull=True)


class MiwoUserAdmin(admin.ModelAdmin):
    list_filter = (InfluencerFollowerListFilter,)
admin.site.register(models.MiwoUser, MiwoUserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Profile, ProfileAdmin)


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
admin.site.register(models.Campaign, CampaignAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
admin.site.register(models.Product, ProductAdmin)


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
admin.site.register(models.ProductImage, ProductImageAdmin)


class PublicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'campaign')
admin.site.register(models.Publication, PublicationAdmin)


class TagVideoAdmin(admin.ModelAdmin):
    list_display = ('publication', 'timestamp', 'product')
admin.site.register(models.TagVideo, TagVideoAdmin)


class DeviceAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Device, DeviceAdmin)
