from django import forms
from .models import User, StatusModel
from django.utils.translation import gettext_lazy as _

STATUS_CHOICES=(
    ("0", "Onay Aşaması"),
    ("1", "Aday"),
    ("2", "Seçildi"),
    ("3", "Tamamlandı")
)

KVKK_CHOICES = ((True, "Evet"), (False, "Hayır"),)

class StatusForm(forms.ModelForm):
    class Meta:
        model=StatusModel
        fields=("status",)

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": _("İsim")}), label=_("İsim"))
    email = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": _("E-Posta")}), label=_("E-Posta"))
    phone = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": _("Telefon")}), label=_("Telefon"))
    message = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "placeholder": _("Mesajınız")}), label=_("Mesajınız"))
    kvkk=forms.BooleanField(widget=forms.CheckboxInput(attrs={"class":"form-check-input"}), label=_("KVKK Metnini okudum ,anladım ve onaylıyorum."), required=True)

class LoginForm(forms.Form):
    class Meta:
        model=User
        fields=("email", "password")

class RegisterForm(forms.Form):
    class Meta:
        model=User
        fields=("email", "username","password")
