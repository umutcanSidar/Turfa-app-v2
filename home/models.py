from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from django.utils.translation import gettext as _
from django.core.validators import FileExtensionValidator

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

from candidate.models import CandidateModel

ROLE_CHOICES = (
    (0, "İşarayan"),
    (1, "İşveren"),
)

PUBLISHED_CHOICES = (
    (False, "Yayında Değil"),
    (True, "Yayında")
)

YES_NO_CHOICES=(
    (0, "Hayır"),
    (1, "Evet")
)


STATUS_CHOICES=(
    ("0", "Onay Aşaması"),
    ("1", "Aday"),
    ("2", "Seçildi"),
    ("3", "Tamamlandı")
)

class Settings(models.Model):
    mail=models.CharField(_("E-Posta"), max_length=200)
    phone=models.CharField(_("Telefon"), max_length=30)
    address= models.CharField(_("Adres"), max_length=300)
    youtube_url= models.CharField(_("YouTube"), max_length=300)
    linkedin_url= models.CharField(_("Linkedin"), max_length=300)
    logo=models.FileField(_("Logo"), upload_to="uploads/", validators=[FileExtensionValidator(['jpg','png', 'svg'])])
    logo_width = models.IntegerField(_("Logo genişliği"), default=200)
    kvkk=RichTextField(_("Kvkk Metni"), blank=True)
    cerez=RichTextField(_("Çerez Politikası Metni"), blank=True)
    role=models.BooleanField(_("Kullanıcı Grubu"), choices=ROLE_CHOICES)

    class Meta:
        verbose_name="Ayarlar"
        verbose_name_plural="Ayarlar"

    def __str__(self):
        if self.role == 0:
            return _("İş arayan")
        else:
            return _("İş veren")

class ContactModel(models.Model):
    content = RichTextField(_("İçerik"))
    content_de = RichTextField(_("İçerik"))
    role=models.BooleanField(_("Kullanıcı Grubu"), choices=ROLE_CHOICES)

    class Meta:
        verbose_name="İletişim"
        verbose_name_plural="İletişimler"

    def __str__(self):
        if self.role == 0:
            return _("İş arayan")
        else:
            return _("İş veren")
 
class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
   
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.BooleanField(_("Kullanıcı Grubu"), choices=ROLE_CHOICES, default=0)
    
    objects=UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name="Kullanıcı"
        verbose_name_plural="Kullanıcılar"

class StatusModel(models.Model):
    candidates=models.ForeignKey(CandidateModel, on_delete=models.CASCADE, blank=True, verbose_name=_("Aday"))
    user=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("İşveren"))
    status=models.CharField(_("Durum"), choices=STATUS_CHOICES, max_length=50)

    class Meta:
        verbose_name="Durum"
        verbose_name_plural="Durumlar"

    def __str__(self):
        return "asd"

class ServiceModel(models.Model):
    title=RichTextField(_("Başlık"))
    title_de=RichTextField(_("Başlık Almanca"))
    text=RichTextUploadingField(_("İçerik"))
    text_de=RichTextUploadingField(_("İçerik Almanca"))
    text_short=RichTextField(_("Kısa Metin"))
    text_short_de=RichTextField(_("Kısa Metin Almanca"))
    slug=models.CharField(_("Slug"), max_length=200)
    img_url = models.FileField(_("Görsel"), upload_to="services/", max_length=100, validators=[FileExtensionValidator(['jpg', 'png'])])
    pdf = models.FileField(_("PDF"), upload_to="services/", max_length=100, validators=[FileExtensionValidator(['pdf'])])
    role=models.BooleanField(_("Kullanıcı Grubu"), choices=ROLE_CHOICES, default=0) 

    class Meta:
        verbose_name="Hizmet"
        verbose_name_plural="Hizmetler"

    def __str__(self):
        return self.title

class BlogModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    title = RichTextField(_("Başlık"), blank=True)
    title_de = RichTextField(_("Başlık Almanca"), blank=True, null=True)
    img_url = models.FileField(_("Görsel"), upload_to="blog/", max_length=100, null=True, blank=True)
    pdf = models.FileField(_("PDF"), upload_to="blog/pdf/", max_length=100, validators=[FileExtensionValidator(['pdf'])], blank=True)
    text = RichTextUploadingField(_("İçerik"), blank=True)
    text_de = RichTextUploadingField(_("İçerik Almanca"), blank=True)
    text_short = RichTextField(_("Kısa içerik"), blank=True)
    text_short_de = RichTextField(_("Kısa içerik Almanca"), blank=False)
    created_at = models.DateField(_("Yayın Tarihi"))
    slug=models.CharField(_("Slug"), max_length=200)
    slug_de=models.CharField(_("Slug Almanca"), max_length=200)
    role = models.BooleanField(_("Kullanıcı Grubu"),choices=ROLE_CHOICES)

    class Meta:
        verbose_name = "Blog yazısı"
        verbose_name_plural = "Blog yazıları"

    def __str__(self):
        return self.title
    
class AboutModel(models.Model):
    title = RichTextField(_("Başlık"), blank=True)
    title_de = RichTextField(_("Başlık Almanca"), blank=True)
    about = RichTextField(_("Hakkında"), blank=True)
    about_de = RichTextField(_("Hakkında Almanca"), blank=True)
    about_alt=RichTextField(_("Hakkında(tam genişlik)"), blank=True)
    about_alt_de=RichTextField(_("Hakkında(tam genişlik) Almanca"), blank=True)
    signf = models.FileField(_("İmza"), upload_to="uploads/about/", max_length=100, null=True, blank=True)
    img_url = models.FileField(_("Görsel"), upload_to="uploads/about/", max_length=100, null=True, blank=True)
    role = models.BooleanField(_("Kullanıcı Grubu"), choices=ROLE_CHOICES, default=0)
    isActive = models.BooleanField(_("Yayın Durumu"), choices=PUBLISHED_CHOICES, default=False)
    
    class Meta: 
        verbose_name = "Hakkında"
        verbose_name_plural = "Hakkında"

    def __str__(self):
        return self.title
