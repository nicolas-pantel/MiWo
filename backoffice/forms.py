from cloudinary.forms import CloudinaryFileField

from django import forms

from . import models


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['picture']

    picture = CloudinaryFileField(
        required=False,
        options={
            'tags': "profile_picture",
            'crop': 'limit', 'width': 150, 'height': 150,
        })

    def clean_picture(self):
        return self.cleaned_data['picture'] or None


class CampaignCreateForm(forms.ModelForm):
    class Meta:
        model = models.Campaign
        fields = ['user', 'name']
        widgets = {
            'user': forms.HiddenInput(),
        }


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput(),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = models.ProductImage
        fields = '__all__'
        widgets = {
            'product': forms.HiddenInput(),
        }

    image = CloudinaryFileField(
        required=False,
        options={
            'tags': "product_image",
            'crop': 'limit', 'width': 500, 'height': 500,
            'eager': [{'crop': 'fill', 'width': 150, 'height': 150}]
        })


class PublicationCreateForm(forms.ModelForm):
    class Meta:
        model = models.Publication
        fields = ['campaign', 'name', 'url']
        widgets = {
            'campaign': forms.HiddenInput(),
        }


class TagVideoCreateForm(forms.ModelForm):
    class Meta:
        model = models.TagVideo
        fields = ['publication', 'timestamp', 'product']
        widgets = {
            'publication': forms.HiddenInput(),
        }
    timestamp = forms.TimeField(initial="00:00:00", widget=forms.TimeInput(attrs={'type': 'time', 'step': 1}))
