from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from .forms import ProfileForm
from . import models


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
    form_class = ProfileForm
    template_name = "account/profile.html"


class CampaignsView(ListView):
    model = models.Campaign
    paginate_by = 20

    def get_queryset(self):
        """Only user's campaigns"""
        return models.Campaign.objects.filter(user=self.request.user)


class CampaignCreateView(CreateView):
    model = models.Campaign
    fields = ['name']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CampaignDeleteView(DeleteView):
    model = models.Campaign
    success_url = reverse_lazy('campaigns')
