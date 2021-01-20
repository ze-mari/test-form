from django import forms
from .models import ApplicationForm


class GeneralForm(forms.Form):

    email = forms.EmailField(label='Емайл', max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        slug = kwargs.get('slug')
        del kwargs['slug']
        super().__init__(*args, **kwargs)
        form = ApplicationForm.objects.get(slug=slug)
        for field in form.form.fields.all():
            self.fields[field.slug] = forms.CharField(label=field.name, max_length=255, required=True)


class ConfirmationForm(forms.Form):

    code = forms.CharField(max_length=4, min_length=4, label='Код подтверждение')











