from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm
from django.views.generic import ListView, DetailView, CreateView
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Ви вдало зареєструвались')
            return redirect('home')
    else:
        form = UserRegisterForm()
        messages.error(request, 'Помилка при реєстрації')
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


class HomeNews(ListView, MyMixin):
    model = News  # Отримуємо всі дані з моделі для сторінки
    template_name = 'news/index.html'  # Передаємо назву темплейта, адже по дефолту шукає файл <model>_<list>.html
    context_object_name = 'news'  # ПО дефолту контекст називається objects_list, а ми переназиваємо
    #extra_context = {'title': 'Головна'}
    #queryset = News.objects.select_related('categoty')  # Використовуємо, якщо не переписуємо запит
    mixin_prop = 'hello world'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # Зберегли в контексті все те, що там було до цього
        context['title'] = 'Головна'
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')  # Отримуємо не всі дані, а тільки ті, які нам потрібні


# def index(request):  # Реквест містить всю інфу про запит та користувача
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список пажилих новин',
#     }
#     return render(request, 'news/index.html', context)


class NewsByCategory(ListView):
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news'  # ПО дефолту контекст називається objects_list, а ми переназиваємо
    allow_empty = False  # Якщо список новину буде пустий, видасть 404 помилку, а не 500
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # Зберегли в контексті все те, що там було до цього
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        # З self витягуємо category_id та вибираємо тільки потрібні дані
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'news/category.html', {'news': news, 'category': category})


class ViewNews(DetailView):
    model = News
    template_name = 'news/view_news.html'
    context_object_name = 'news_item'


# def view_news(request, news_id):
#     #news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'news_item': news_item})


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    login_url = '/admin/'  # Вказує, куди перенаправляти юзера, якщо він не залогінився
    raise_exception = True  # 403 якщо юзера не авторизований


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)  # Забираємо дані з реквеста
#         if form.is_valid():
#             #news = News.objects.create(**form.cleaned_data)  # ** розпаковує солвник і відповідним ключає дає відповідні значенння
#             news = form.save()
#             return redirect(news)  # ПОвертаємось на сторінку ствоерної новини
#     else:
#         form = NewsForm()  # Якщо ми не посилаємо дані, то просто відображаємо форму
#     return render(request, 'news/add_news.html', {'form': form})
