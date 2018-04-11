from cloudinary.forms import CloudinaryFileField

from django.forms import ModelForm

from .models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['picture', 'public_name']

    picture = CloudinaryFileField(
        options={
            'tags': "profile_picture",
            'crop': 'limit', 'width': 1000, 'height': 1000,
            'eager': [{'crop': 'fill', 'width': 150, 'height': 150}]
        })
