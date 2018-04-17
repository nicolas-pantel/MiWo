from cloudinary.forms import CloudinaryFileField

from django import forms

from . import models


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['picture', 'public_name']

    picture = CloudinaryFileField(
        required=False,
        options={
            'tags': "profile_picture",
            'crop': 'limit', 'width': 1000, 'height': 1000,
            'eager': [{'crop': 'fill', 'width': 150, 'height': 150}]
        })


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
