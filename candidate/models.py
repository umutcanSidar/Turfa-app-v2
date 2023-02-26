from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _


# Create your models here.
MARTIAL_CHOICES=(
    (False, "Bekar"),
    (True, "Evli"),
)

STATUS_CHOICES=(
    ("0", "Onay Aşaması"),
    ("1", "Aday"),
    ("2", "Seçildi"),
    ("3", "Tamamlandı")
)

GERMAN_CHOICES = (
    ("0", "A0"),
    ("1", "A1"),
    ("2", "A2"),
    ("3", "B1"),
    ("4", "B2"),
)

class CandidateModel(models.Model):
    name=models.CharField(_("Ad"), max_length=100)
    surname=models.CharField(_("Soyad"), max_length=100)
    email=models.EmailField(_("E-Posta"), max_length=150)
    phone=models.CharField(_("Telefon"), max_length=15)
    tc=models.CharField(_("TC Kimlik Numarası"), max_length=11)
    children=models.IntegerField(_("Çocuk Sayısı"), null=True)
    birthday=models.DateField(_("Doğum Tarihi"), blank=True)
    martial_status=models.BooleanField(_("Medeni Durumu"), choices=MARTIAL_CHOICES, default=False)
    city=models.CharField(_("Şehir"), max_length=100)
    postcode=models.CharField(_("Posta Kodu"), max_length=6)
    address=models.CharField(_("Adres"), max_length=200)
    photo=models.FileField(_("Fotoğraf"), upload_to="uploads/isarayan/", validators=[FileExtensionValidator(['jpg','svg','png'])], blank=True)
    german=models.CharField(_("Almanca"), choices=GERMAN_CHOICES, max_length=50, blank=True, null=True)
    status=models.CharField(_("Durumu"), choices=STATUS_CHOICES, max_length=50, default="0")

    class Meta:
        verbose_name="Aday Formu"
        verbose_name_plural="Aday Formları"

    def __str__(self):
        return self.email


class ExperienceModel(models.Model):
    institution_name = models.CharField(_("Kurum Adı"), max_length=100)
    position=models.CharField(_("Mevki"), max_length=100)
    work_address=models.CharField(_("İş Adresi"), max_length=250)
    ref_name=models.CharField(_("Referans Adı"), max_length=100)
    institution_email=models.EmailField(_("Kurum Email"))
    institution_phone=models.CharField(_("Kurum Telefonu"), max_length=150)
    entry_date = models.DateField(_("Giriş Tarihi"), null=True)
    quit_date = models.DateField(_("Çıkış Tarihi"), null=True)
    candidate = models.ForeignKey(CandidateModel, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name="Deneyim"
        verbose_name_plural="Deneyimler"

    def __str__(self):
        return self.institution_name

class EducationModel(models.Model):
    university_name = models.CharField(_("Üniversite Adı"), max_length=100)
    departman=models.CharField(_("Mezun Olunan Bölüm"), max_length=150)
    doctorate=models.CharField(_("Doktora Yaptınız Mı?"), max_length=100)
    degree=models.CharField(_("Yüksek Lisans Yaptınız Mı?"), max_length=100)
    phd=models.CharField(_("Doktorlar İçin Uzmanlık Alanı"), max_length=100)
    entry_date = models.DateField(_("Üniversiteye Giriş Tarihi"), null=True)
    graduated_at = models.DateField(_("Mezuniyet Tarihi"), null=True)
    candidate = models.ForeignKey(CandidateModel, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name="Eğitim"
        verbose_name_plural="Eğitimler"

    def __str__(self):
        return self.university_name


