from .models import Uzsakymas, UzsakymasReview
from django import forms
from .models import Profilis
from django import forms
from django.contrib.auth.models import User


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['nuotrauka']

class DateInput(forms.DateInput):
    input_type = 'date'

class UserUzsakymasCreateForm(forms.ModelForm):
    class Meta:
        model = Uzsakymas
        fields = ['preke_id', 'vartotojas']
        widgets = {'vartotojas': forms.HiddenInput()}

class UzsakymasReviewForm(forms.ModelForm):
    class Meta:
        model = UzsakymasReview
        fields = ('content', 'uzsakymas', 'vartotojas',)
        widgets = {"uzsakymas": forms.HiddenInput(), "vartotojas": forms.HiddenInput()}
