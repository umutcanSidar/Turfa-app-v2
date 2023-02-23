from django import forms
from django.utils.translation import gettext as _
from .models import CandidateModel, ExperienceModel, EducationModel

# class CandidateForm(forms.Form):
#     name = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": _("Ad")}), label=_("Ad"))
#     surname = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": _("Soyad")}), label=_("Soyad"))
#     email = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": _("E-Posta")}), label=_("E-Posta"))
#     phone = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": _("Telefon")}), label=_("Telefon"))
#     children = forms.IntegerField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": _("Doğum Tarihi")}), label=_("Doğum Tarihi"))
#     tc = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": _("TC Kimlik Numarası")}), label=_("TC Kimlik Numarası"))
#     postcode = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": _("Posta Kodu")}), label=_("Posta Kodu"))
#     address=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":_("Adres")}), label=_("Adres"))
#     photo=forms.FileField(widget=forms.FileInput(attrs={"class":"form-control", "placeholder": _("Fotoğraf")}), label=_("Fotoğraf"))
    
#     def __init__(self, user, *args, **kwargs):
#         super(CandidateForm, self).__init__(*args, **kwargs)
#         self.fields['test_field'] = forms.CharField(max_length=250)

class CandidateForm(forms.ModelForm):
    class Meta:
        model= CandidateModel
        fields=('name','surname','email', 'phone', 'tc', 'children', 'birthday', 'martial_status', "city", "postcode", "photo","address")
        widgets= {
            'birthday': forms.SelectDateWidget(attrs={'class':'form-control'}, years=range(1970, 2001)),
            'children': forms.TextInput(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CandidateForm, self).__init__(*args, **kwargs)
        
        for field,f in self.fields.items():
            f.widget.attrs['class'] = "form-control"
            f.widget.attrs['placeholder'] = f.label
        
class EducationForm(forms.ModelForm):
    class Meta:
        model= EducationModel
        fields=('university_name', 'departman', 'doctorate', 'degree', 'entry_date','graduated_at', 'phd')
        widgets={
            'graduated_at': forms.SelectDateWidget(attrs={'class':'form-control'}, years=range(1970, 2023)),
            'entry_date': forms.SelectDateWidget(attrs={'class':'form-control'}, years=range(1970, 2024)),
        }


    def __init__(self, *args, **kwargs):
        super(EducationForm, self).__init__(*args, **kwargs)
        
        for field,f in self.fields.items():
            f.widget.attrs['class'] = "form-control"
            f.widget.attrs['placeholder'] = f.label
            f.label=""
            

class ExperienceForm(forms.ModelForm):
    class Meta:
        fields=('institution_name', 'position', 'work_address', 'ref_name', 'institution_email', 'institution_phone', 'entry_date', 'quit_date')
        model= ExperienceModel
        widgets = {
            'entry_date': forms.SelectDateWidget(attrs={'class':'form-control'}, years=range(1970, 2024)),
            'quit_date': forms.SelectDateWidget(attrs={'class':'form-control'}, years=range(1970, 2024)),
        }
       
    def __init__(self, *args, **kwargs):
        super(ExperienceForm, self).__init__(*args, **kwargs)
        
        for field,f in self.fields.items():
            f.widget.attrs['class'] = "form-control"
            f.widget.attrs['placeholder'] = f.label
            f.label=""
        