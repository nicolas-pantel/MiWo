from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from . import forms, models


class IndexView(TemplateView):
    template_name = "backoffice/index.html"


class DemoView(TemplateView):
    template_name = "backoffice/demo.html"


class DemoServerView(View):
    """Send a simple message to channels groups"""
    def get(self, request, channel, *args, **kwargs):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            channel,
            {"type": "influencer.broadcast", "text": "Message sent from influencer " + channel[-1]},
        )
        return JsonResponse({'response': 'ok'})


def profile(request):
    return redirect("profile_update", pk=request.user.profile.pk)


class ProfileUpdateView(UpdateView):
    model = models.Profile
    form_class = forms.ProfileForm
    template_name = "account/profile.html"
    extra_context = {"navtop": "profile"}


# CAMPAIGNS ###

class CampaignMixin(object):
    model = models.Campaign
    extra_context = {"navtop": "campaigns"}


class CampaignsView(CampaignMixin, ListView):
    paginate_by = 20

    def get_queryset(self):
        """Only user's campaigns"""
        return models.Campaign.objects.filter(user=self.request.user)


class CampaignCreateView(CampaignMixin, CreateView):
    form_class = forms.CampaignCreateForm

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super().get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['user'] = self.request.user.pk
        return initial


class CampaignDeleteView(CampaignMixin, DeleteView):
    success_url = reverse_lazy('campaigns')


class CampaignUpdateView(CampaignMixin, UpdateView):
    fields = ['name']


# PRODUCTS ###

class ProductMixin(object):
    model = models.Product
    extra_context = {"navtop": "products"}


class ProductsView(ProductMixin, ListView):
    paginate_by = 20

    def get_queryset(self):
        """Only user's products"""
        return models.Product.objects.filter(user=self.request.user)


class ProductCreateView(ProductMixin, CreateView):
    form_class = forms.ProductCreateForm

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super().get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['user'] = self.request.user.pk
        return initial


class ProductDeleteView(ProductMixin, DeleteView):
    success_url = reverse_lazy('products')


class ProductUpdateView(ProductMixin, UpdateView):
    fields = ['name', 'description', 'price']
