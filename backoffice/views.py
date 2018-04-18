from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from . import forms, models


class IndexView(TemplateView):
    template_name = "backoffice/index.html"


class DemoView(LoginRequiredMixin, TemplateView):
    template_name = "backoffice/demo.html"


class DemoServerView(LoginRequiredMixin, View):
    """Send a simple message to channels groups"""
    def get(self, request, channel, *args, **kwargs):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            channel,
            {"type": "influencer.broadcast", "text": "Message sent from influencer " + channel[-1]},
        )
        return JsonResponse({'response': 'ok'})


@login_required
def profile(request):
    return redirect("profile_update", pk=request.user.profile.pk)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Profile
    form_class = forms.ProfileForm
    template_name = "account/profile.html"
    extra_context = {"navtop": "profile"}


# CAMPAIGNS ###

class CampaignMixin(LoginRequiredMixin):
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

class ProductMixin(LoginRequiredMixin):
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

    def get_context_data(self, **kwargs):
        """Add empty product image form"""
        context = super().get_context_data(**kwargs)
        context["image_form"] = forms.ProductImageForm({"product": self.object})
        context["posted"] = context["image_form"].instance
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ProductImageCreateView(LoginRequiredMixin, CreateView):
    model = models.ProductImage
    form_class = forms.ProductImageForm

    def post(self, request, *args, **kwargs):
        form = forms.ProductImageForm(request.POST, request.FILES)
        if form.is_valid() and request.FILES:
            form.save()
        return redirect("product_update", pk=request.POST["product"])


@login_required
def product_image_delete_view(request, product_pk, product_image_pk):
    product_image = models.ProductImage.objects.get(pk=product_image_pk)
    product_image.delete()
    return redirect("product_update", pk=product_pk)


# PUBLICATIONS ###

class PublicationMixin(LoginRequiredMixin):
    model = models.Publication
    extra_context = {"navtop": "campaigns"}


class PublicationListView(PublicationMixin, ListView):
    """Influencer publications list"""
    paginate_by = 20

    def get_queryset(self):
        """Only campaign's publications"""
        return models.Publication.objects.filter(campaign=self.kwargs["campaign_pk"])

    def get_context_data(self, **kwargs):
        """Add campaign id"""
        context = super().get_context_data(**kwargs)
        context["campaign_pk"] = self.kwargs["campaign_pk"]
        return context


class PublicationCreateView(PublicationMixin, CreateView):
    form_class = forms.PublicationCreateForm

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super().get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['campaign'] = self.kwargs["campaign_pk"]
        return initial

    def get_context_data(self, **kwargs):
        """Add campaign id"""
        context = super().get_context_data(**kwargs)
        context["campaign_pk"] = self.kwargs["campaign_pk"]
        return context


class PublicationDeleteView(PublicationMixin, DeleteView):

    def get_success_url(self):
        return reverse("publications", kwargs={"campaign_pk": self.kwargs["campaign_pk"]})


class PublicationUpdateView(PublicationMixin, UpdateView):
    fields = ['name', 'url']

    def get_context_data(self, **kwargs):
        """Add campaign id"""
        context = super().get_context_data(**kwargs)
        context["campaign_pk"] = self.kwargs["campaign_pk"]
        return context
