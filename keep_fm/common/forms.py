from django import forms
from keep_fm.users.models import User


class CombinedRankingForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
