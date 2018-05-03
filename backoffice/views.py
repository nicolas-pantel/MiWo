from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import urbanairship as ua

from allauth.account import views as allauth_views

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.formsets import formset_factory
from django.http import JsonResponse
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, View, ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView

from . import forms, models
from .external_api_clients import youtube


def index(request):
    if not request.user.is_authenticated:
        return redirect("index_signup")
    else:
        return redirect("publication_step1")


class IndexView(FormView):
    template_name = "backoffice/index.html"
    form_class = forms.EmailForm
    success_url = reverse_lazy("signup_step2")

    def post(self, request, *args, **kwargs):
        request.session['email'] = request.POST.get('email')
        request.session['sub_funnel'] = True
        return super().post(request, *args, **kwargs)


class SignUpStep2View(TemplateView):
    template_name = "backoffice/step2.html"


class SignUpStep3View(allauth_views.SignupView):
    template_name = "account/signup.html"
    form_class = forms.SignupForm
    success_url = reverse_lazy("profile")

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super().get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['email'] = self.request.session['email']
        return initial


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
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        """Add user names form"""
        context = super().get_context_data(**kwargs)
        context["user_names_form"] = forms.UserNamesForm(initial={
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
        })
        return context

    def post(self, request, *args, **kwargs):
        """Process user names form"""
        resp = super().post(request, *args, **kwargs)
        form = forms.UserNamesForm(request.POST)
        if form.is_valid():
            request.user.first_name = form.cleaned_data["first_name"]
            request.user.last_name = form.cleaned_data["last_name"]
            request.user .save()
            request.session['sub_funnel'] = False
        return resp


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
    publication_funnel = False

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super().get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['user'] = self.request.user.pk
        return initial

    def get_success_url(self):
        if self.publication_funnel:
            return reverse("publication_step2", kwargs={'campaign_pk': self.object.pk})
        else:
            return super().get_success_url()


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
    form_class = forms.ProductUpdateForm

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super().get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['date_from'] = timezone.now().date()
        initial['date_to'] = (timezone.now() + timezone.timedelta(days=7)).date()
        initial['user'] = self.request.user.pk
        return initial

    def get_context_data(self, **kwargs):
        """Add empty product image form"""
        context = super().get_context_data(**kwargs)
        context["image_form"] = forms.ProductImageForm({"product": self.object})
        context["posted"] = context["image_form"].instance
        return context


class JSONProductCreateView(ProductMixin, CreateView):
    form_class = forms.ProductCreateForm

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        post = self.request.POST.copy()
        post['form-0-product'] = self.object.pk
        post['form-1-product'] = self.object.pk
        post['form-2-product'] = self.object.pk
        ProductImageFormset = formset_factory(forms.ProductImageForm)
        image_formset = ProductImageFormset(post, self.request.FILES)
        if image_formset.is_valid():
            for image_form in image_formset:
                if image_form.is_valid():
                    image_form.save()

        return self.render_to_response(self.get_context_data(form=form))

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(self.get_data(context), **response_kwargs)

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        if self.object:
            return {'product_pk': self.object.pk, 'product_name': self.object.name}
        else:
            return {'product_pk': ''}


class ProductDeleteView(ProductMixin, DeleteView):
    success_url = reverse_lazy('products')


class ProductUpdateView(ProductMixin, UpdateView):
    form_class = forms.ProductUpdateForm

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super().get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['date_from'] = timezone.now().date()
        initial['date_to'] = (timezone.now() + timezone.timedelta(days=7)).date()
        initial['user'] = self.request.user.pk
        return initial

    def get_context_data(self, **kwargs):
        """Add empty product image form"""
        context = super().get_context_data(**kwargs)
        context["image_form"] = forms.ProductImageForm({"product": self.object})
        context["posted"] = context["image_form"].instance
        return context


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
    publication_funnel = False

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
        context["youtube_videos"] = youtube.videos_list(self.request.user)
        return context

    def get_success_url(self):
        if self.publication_funnel:
            return reverse("tagvideo_create", kwargs={'publication_pk': self.object.pk})
        else:
            return super().get_success_url()


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


@login_required
def publish_publication(request, pk):
    """Send notifaction to followers"""
    airship = ua.Airship(settings.URBANAIRSHIP_KEY, settings.URBANAIRSHIP_MASTER_SECRET)
    push = airship.create_push()
    push.notification = ua.notification(
        ios=ua.ios(
            alert="New publication from {}".format(request.user.username),
            badge='+1',
        )
    )
    push.device_types = ua.device_types('ios')
    followers = request.user.followers.all()
    for follower in followers:
        devices = models.Device.objects.filter(profile=follower.profile)
        if devices.exists():
            device = devices[0]
        push.audience = ua.ios_channel(device.chanid)
        push.send()
    # Record as published and redirect to publications list
    publication = models.Publication.objects.get(pk=pk)
    publication.published = True
    publication.save()
    return redirect("campaigns")


class TagVideoMixin(LoginRequiredMixin):
    model = models.TagVideo
    extra_context = {"navtop": "campaigns"}


class TagVideoListView(TagVideoMixin, ListView):
    paginate_by = 20

    def get_queryset(self):
        """Only publication's tags"""
        return models.TagVideo.objects.filter(publication=self.kwargs["publication_pk"])

    def get_context_data(self, **kwargs):
        """Add publication id"""
        context = super().get_context_data(**kwargs)
        context["publication_pk"] = self.kwargs["publication_pk"]
        context["form"] = forms.TagVideoCreateForm()
        return context

    def post(self, request, *args, **kwargs):
        """Process tag form"""
        self.object_list = self.get_queryset()
        form = forms.TagVideoCreateForm(request.POST, initial={"publication": self.kwargs["publication_pk"]})
        if form.is_valid():
            form.save()
        return self.render_to_response(self.get_context_data())


class TagVideoCreateView(TagVideoMixin, CreateView):
    paginate_by = 20
    form_class = forms.TagVideoCreateForm

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super().get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['publication'] = self.kwargs["publication_pk"]
        return initial

    def get_context_data(self, **kwargs):
        """Add tags list and publication"""
        context = super().get_context_data(**kwargs)
        # Limit products to user's
        context["form"].fields["product"].queryset = models.Product.objects.filter(user=self.request.user)
        # Add publication and tags ist
        publication = models.Publication.objects.get(pk=self.kwargs["publication_pk"])
        context["publication"] = publication
        context["tags_list"] = publication.tags_video.all()

        # Add product creation form
        context["product_create_form"] = forms.ProductCreateForm(initial={
            'user': self.request.user.pk,
            'date_from': timezone.now().date(),
            'date_to': (timezone.now() + timezone.timedelta(days=7)).date(),
        })

        # Add image product creation formset
        context["image_formset"] = formset_factory(forms.ProductImageForm, extra=3)
        return context


class TagVideoDeleteView(TagVideoMixin, DeleteView):

    def get_success_url(self):
        return reverse('tagvideo_create', kwargs={"publication_pk": self.object.publication.pk})
