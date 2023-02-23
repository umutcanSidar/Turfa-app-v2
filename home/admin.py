from django.contrib import admin
from .models import ServiceModel, BlogModel, AboutModel, User, ContactModel, Settings, StatusModel
from django.utils.translation import gettext as _

# INLINES
admin.site.site_header = "TÜRFA Admin"
admin.site.site_title = "TÜRFA Admin Portal"
admin.site.index_title = "Welcome to TÜRFA Portal"

# MODELS
@admin.register(StatusModel)
class StatusAdmin(admin.ModelAdmin):
    list_display=("get_user_name", "candidates_name", "status")

    def get_user_name(self, obj):
        return obj.user

    def candidates_name(self, obj):
        return obj.candidates.email
    
    candidates_name.short_description = _('E-Posta')
    candidates_name.admin_order_field = 'candidates__name'
    get_user_name.short_description = _('İşveren')


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