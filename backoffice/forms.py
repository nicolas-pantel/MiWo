from cloudinary.forms import CloudinaryFileField

from allauth.account import forms as allauth_forms

from django import forms

from . import models


class EmailForm(forms.ModelForm):
    class Meta:
        model = models.MiwoUser
        fields = ['email']


class UserKindForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['kind']


class UserNamesForm(forms.ModelForm):
    class Meta:
        model = models.MiwoUser
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'autofocus': True})
        }


class SignupForm(allauth_forms.SignupForm):
    email = forms.EmailField(widget=forms.HiddenInput())


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['picture', 'company_name', 'country']

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


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput(),
            'date_from': forms.DateInput(),
            'date_to': forms.DateInput(),
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
