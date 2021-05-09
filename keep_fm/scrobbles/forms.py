from django import forms
from keep_fm.users.models import User


class CombinedRankingForm(forms.Form):
    """
    CombinedRankingForm is used to select another User from a dropdown,
    to create a combined ranking of logged in user and the selected one.
    """

    user = forms.ModelChoiceField(queryset=User.objects.all())
