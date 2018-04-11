from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View

from .forms import ProfileForm
from .models import Profile


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


@login_required
def profile(request):
    profiles = Profile.objects.filter(user=request.user)
    if profiles.exists():
        context = dict(backend_form=ProfileForm(instance=profiles[0]))
        context['profile'] = profiles[0]
    else:
        context = dict(backend_form=ProfileForm())

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        context['posted'] = form.instance
        if form.is_valid():
            if profiles.exists():
                profile = form.save(instance=profiles[0], commit=False)
            else:
                profile = form.save(commit=False)
                profile.user = request.user
            profile.save()

    return render(request, 'account/profile.html', context)
