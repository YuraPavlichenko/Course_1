from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True) #Тобто, заповнюватись дата буде тільки при створенні,але не при редагвані
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/',
                              blank=True)  # upload_to сказує,куди ми будемо загружати файли, будемо в рік/міс/ден
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категорія')
    views = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('view_news', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новина'  # Назва моделі в однині
        verbose_name_plural = 'Новини'  # В множині
        ordering = ['title', 'created_at']


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Назва категорії')  # db_index індексує поле

    def get_absolute_url(self):
        # Перший параметром указуємо маршрут в urls, куди ми хочемо йти, тобто category
        return reverse('category', kwargs={'category_id': self.pk})  # Другий параметр - те, що використовується при формуванні url

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категорія'  # Назва моделі в однині
        verbose_name_plural = 'Категорії'  # В множині
        ordering = ['title']