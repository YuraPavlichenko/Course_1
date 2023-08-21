from django.contrib import admin
from .models import News, Category


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created_at', 'updated_at', 'is_published')  # Поля, які будуть показані в адмінці
    list_display_links = ('id', 'title')  # Поля, які будуть посиланнями
    search_fields = ('title', 'content')  # Поля, за якими можна шукати
    list_editable = ('is_published',)  # Можемо реадгувати, не щзаходячи в саму новину
    list_filter = ('is_published', 'category')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')  # Поля, які будуть показані в адмінці
    list_display_links = ('id', 'title')  # Поля, які будуть посиланнями
    search_fields = ('title',)  # Поля, за якими можна шукати


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Тайтл'
admin.site.site_header = 'Хедер'