from django.contrib import admin
from .models import Category, Instrument, Expert, LearningContent, Contact, Tutorial, TunerConfiguration, Branding

admin.site.site_header = 'BAJAGHAR Administration'
admin.site.site_title = 'BAJAGHAR Admin'
admin.site.index_title = 'Content Management'


def delete_selected_with_cascade(modeladmin, request, queryset):
    """Custom action to delete selected items and cascade dependents"""
    queryset.delete()

delete_selected_with_cascade.short_description = 'Delete selected items and related data'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    actions = [delete_selected_with_cascade]


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'region', 'is_featured', 'show_tuner', 'created_at')
    list_filter = ('category', 'region', 'is_featured', 'show_tuner')
    search_fields = ('name', 'description', 'history')
    actions = [delete_selected_with_cascade]
    fieldsets = (
        (None, {'fields': ('name', 'name_ne', 'category', 'region', 'region_ne', 'description', 'description_ne')}),
        ('Content', {'fields': ('history', 'history_ne', 'materials', 'materials_ne', 'playing_technique', 'playing_technique_ne', 'cultural_significance', 'cultural_significance_ne')}),
        ('Media', {'fields': ('primary_image', 'model_3d', 'show_brightness_control')}),
        ('Display', {'fields': ('is_featured', 'show_tuner')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')

    def get_inline_instances(self, request, obj=None):
        if obj is None or not getattr(obj, 'show_tuner', False):
            return []
        return super().get_inline_instances(request, obj)


class TunerConfigurationInline(admin.StackedInline):
    model = TunerConfiguration
    can_delete = False
    verbose_name = 'Tuner configuration'
    verbose_name_plural = 'Tuner configuration'
    fk_name = 'instrument'
    max_num = 1
    fields = ('tuning_name', 'tuning_name_ne', 'notes', 'frequencies', 'is_default')

    def has_add_permission(self, request, obj=None):
        return True


InstrumentAdmin.inlines = getattr(InstrumentAdmin, 'inlines', ()) + (TunerConfigurationInline,)


@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    list_display = ('name', 'expertise', 'contact_email', 'created_at')
    search_fields = ('name', 'expertise', 'bio')
    filter_horizontal = ('instruments',)
    actions = [delete_selected_with_cascade]
    fieldsets = (
        (None, {'fields': ('name', 'name_ne', 'expertise', 'expertise_ne', 'contact_email')}),
        ('Biography', {'fields': ('bio', 'bio_ne', 'detailed_bio', 'detailed_bio_ne')}),
        ('Achievements', {'fields': ('achievements', 'achievements_ne')}),
        ('Instruments', {'fields': ('instruments',)}),
        ('Timestamps', {'fields': ('photo', 'created_at')}),
    )
    readonly_fields = ('created_at',)


@admin.register(LearningContent)
class LearningContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_published', 'updated_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'content')
    actions = [delete_selected_with_cascade]
    fieldsets = (
        (None, {'fields': ('title', 'title_ne', 'order', 'is_published')}),
        ('Content', {'fields': ('content', 'content_ne')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'ip_address', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'ip_address', 'is_read', 'created_at')
    actions = [delete_selected_with_cascade]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ('title', 'instrument', 'instructor_name', 'duration', 'created_at')
    list_filter = ('instrument', 'created_at')
    search_fields = ('title', 'instructor_name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    actions = [delete_selected_with_cascade]
    fieldsets = (
        (None, {'fields': ('instrument', 'title', 'title_ne', 'description', 'description_ne')}),
        ('Video & Instructor', {'fields': ('video_url', 'instructor_name', 'instructor_name_ne', 'duration')}),
        ('Captions', {'fields': ('caption_en', 'caption_ne')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(Branding)
class BrandingAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_ne', 'contact_email', 'updated_at')
    search_fields = ('name', 'name_ne', 'contact_email')
    fieldsets = (
        (None, {'fields': ('name', 'name_ne', 'logo', 'logo_alt', 'logo_alt_ne', 'contact_email')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')
    actions = [delete_selected_with_cascade]

    def has_add_permission(self, request):
        return not Branding.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False



