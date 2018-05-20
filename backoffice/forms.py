from cloudinary.forms import CloudinaryFileField

from allauth.account import forms as allauth_forms

from django import forms

from . import models


# Specific Fields
class UTF8CloudinaryFileField(CloudinaryFileField):
    """Manage UTF8 filenames"""
    def to_python(self, value):
        """Encode filenames with accents"""
        if value:
            value.name = value.name.encode('utf-8')
        return super().to_python(value)


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
        fields = ['username', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'autofocus': True})
        }


class SignupForm(allauth_forms.SignupForm):
    email = forms.EmailField(widget=forms.HiddenInput())


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['picture', 'company_name', 'country']

    picture = UTF8CloudinaryFileField(
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
        fields = ['user', 'name', 'description', 'price', 'date_from', 'date_to', 'referal_link']
        widgets = {
            'user': forms.HiddenInput(),
            'date_from': forms.DateInput(),
            'date_to': forms.DateInput(),
        }


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ['user', 'name', 'description', 'price', 'date_from', 'date_to', 'referal_link']
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

    image = UTF8CloudinaryFileField(
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
    product = forms.ModelChoiceField(queryset=models.Product.objects.all(), empty_label="Choose a smartlink")
