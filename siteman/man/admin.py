from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from man.models import Man, Category


class MarriedFilter(admin.SimpleListFilter):
    title = 'Status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'zamuzhem'),
            ('single', 'nezamuzhem')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        if self.value() == 'single':
            return queryset.filter(husband__isnull=True)

@admin.register(Man)
class ManAdmin(admin.ModelAdmin):
    fields = ['title', 'content', 'slug', 'photo', 'post_photo', 'cat', 'husband', 'tags']
    readonly_fields = ['post_photo']
    prepopulated_fields = {"slug": ("title", )}
    filter_vertical = ['tags']
    list_display = ('title', 'post_photo', 'time_create', 'is_active', 'cat')
    list_display_links = ('title', )
    ordering = ['-time_create', 'title']
    list_editable = ('is_active', )
    list_per_page = 5
    actions = ['set_active', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = [MarriedFilter, 'cat__name', 'is_active']
    save_on_top = True

    @admin.display(description='Image', ordering='content')
    def post_photo(self, man: Man):
        if man.photo:
            return mark_safe(f'<img src="{man.photo.url}" width=50>')
        return 'Without photo'

    @admin.action(description='Publish selected posts')
    def set_active(self, request, queryset):
        count = queryset.update(is_active=Man.Status.PUBLISHED)
        self.message_user(request, f'Change {count} posts.')

    @admin.action(description='Remove from publication')
    def set_draft(self, request, queryset):
        count = queryset.update(is_active=Man.Status.DRAFT)
        self.message_user(request, f'{count} remove from publication.', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
