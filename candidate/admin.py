from django.contrib import admin
from .models import ExperienceModel, EducationModel, CandidateModel
from home.models import StatusModel
# Register your models here.
@admin.register(StatusModel)
class StatusAdmin(admin.ModelAdmin):
    pass

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
    list_display=("name", "surname","phone", "email")

@admin.register(ExperienceModel)
class ExperienceAdmin(admin.ModelAdmin):
    pass

@admin.register(EducationModel)
class EducationAdmin(admin.ModelAdmin):
    pass