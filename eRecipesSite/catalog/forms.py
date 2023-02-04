import datetime
from datetime import date

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class UpdateLastMadeForm(forms.Form):
    years = list(range(2010,2024))
    last_made = forms.DateField(help_text="Enter the date the recipe was last made.",widget=forms.SelectDateWidget(years = years))

    def clean_last_made(self):
        data = self.cleaned_data['last_made']

        # Check if a date is not in the past.
        if data > datetime.date.today():
            raise ValidationError(_('Invalid date - date in the future'))

        # Check if a date is in the allowed range (+4 weeks from today).
        # if data > datetime.date.today() + datetime.timedelta(weeks=4):
        #     raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data



# from django.forms import ModelForm

# from catalog.models import Recipe

# class UpdateLastMadeForm(ModelForm):
#     def clean_last_made(self):
#        data = self.cleaned_data['last_made']

#        # Check if a date is not in the past.
#        if data > datetime.date.today():
#            raise ValidationError(_('Invalid date - date in the future'))

#     #    # Check if a date is in the allowed range (+4 weeks from today).
#     #    if data > datetime.date.today() + datetime.timedelta(weeks=4):
#     #        raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

#        # Remember to always return the cleaned data.
#        return data

#     class Meta:
#         model = Recipe
#         fields = ['last_made']
#         labels = {'last_made': _('Last made')}
#         help_texts = {'last_made': _('Enter when the recipe was last made.')}




