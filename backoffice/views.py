from django.http import JsonResponse
from django.views.generic import TemplateView, View

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


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
