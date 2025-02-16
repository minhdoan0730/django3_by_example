from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django import forms
from .models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image  # inhetir from Image model
        fields = ('title', 'url', 'description')  # only 3 field
        widgets = {
            'url': forms.HiddenInput,
            # this widge will rendered html type="hidden"
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        # cleaned data is dictionary data in for

        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError(
                'The given URL does not '
                'match valid image extensions.')
        return url
    # enddef

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super(ImageCreateForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(
            slugify(image.title),
            image_url.rsplit('.', 1)[1].lower())
        # download image from the given URL

        response = request.urlopen(image_url)
        image.image.save(
            image_name,
            ContentFile(response.read()),
            save=False)
        if commit:
            image.save()
        return image
    # enddef
# endclass
