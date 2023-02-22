from django import forms
from django.utils.translation import gettext as _
from .models import User, StatusModel

STATUS_CHOICES=(
    (True, "Aday"),
    (False, "Seçildi")
)

class StatusForm(forms.ModelForm):
    class Meta:
        model=StatusModel
        fields=("status",)

        

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": _("İsim")}), label=_("İsim"))
    email = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": _("E-Posta")}), label=_("E-Posta"))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": _("Telefon")}), label=_("Telefon"))
    message = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "placeholder": _("Mesajınız")}), label=_("Mesajınız"))

class LoginForm(forms.Form):
    class Meta:
        model=User
        fields=("email", "password")

class RegisterForm(forms.Form):
    class Meta:
        model=User
        fields=("email", "username","password")
