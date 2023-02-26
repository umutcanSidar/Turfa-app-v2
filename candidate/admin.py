from django.contrib import admin
from .models import ExperienceModel, EducationModel, CandidateModel
from django.utils.safestring import mark_safe
from django.urls import path, reverse
from .views import CvView

class ExperienceInline(admin.TabularInline):
    model=ExperienceModel

class EducationInline(admin.TabularInline):
    model=EducationModel

@admin.register(CandidateModel)
class CandidateAdmin(admin.ModelAdmin):
    inlines=[
        ExperienceInline,
        EducationInline
    ]

    search_fields=["name","email",]
    list_display=("name", "surname","phone", "email", "button")

    def get_urls(self):
        return [
            path( "<pk>/cv",
                self.admin_site.admin_view(CvView.as_view()),
                name=f"cv",
            ),
            *super().get_urls(),
        ]

    def button(self, obj):
        url = reverse("admin:cv", args=[obj.pk])
        return mark_safe(f'<a href="{url}" target="_blank">PDF İndir</a>')
    
    button.short_description = 'PDF'
    button.allow_tags = True

@admin.register(ExperienceModel)
class ExperienceAdmin(admin.ModelAdmin):
    pass

@admin.register(EducationModel)
class EducationAdmin(admin.ModelAdmin):
    pass

