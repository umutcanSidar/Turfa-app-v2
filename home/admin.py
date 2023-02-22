from django.contrib import admin
from .models import ServiceModel, BlogModel, AboutModel, User, ContactModel, Settings, StatusModel


# INLINES


# MODELS
@admin.register(StatusModel)
class StatusAdmin(admin.ModelAdmin):
    list_display=("user", "candidates", "status")


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    pass

@admin.register(ContactModel)
class ContactAdmin(admin.ModelAdmin):
    pass

@admin.register(ServiceModel)
class ServiceAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'last_login')}),
        ('Permissions', {'fields': ( 
            'role',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('email', 'role', 'last_login')
    list_filter = ('role',)
    search_fields = ('email',)
    ordering = ('email',)

@admin.register(BlogModel)
class BlogAdmin(admin.ModelAdmin):
    pass

@admin.register(AboutModel)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("title", "role")



# REGISTERED