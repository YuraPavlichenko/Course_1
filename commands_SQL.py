News.objects.all() - Отримуємо всі дані з моделі

News.objects.order_by('Поле таблиці') - Сортуємо по певному полю, якщо поставити мінус перед атрибутом,
сортування відбудеться в оберненому порядку

Метод reverse() - також міняє порядок на протилежний

News.objects.get(pk=1) - отримуємо тільки один запис з певним параметром

variable = _    Означає, що ми присвоюємо змінній останній результат вибірки

Category у нас первинна модель, бо нна неї посилаються. Якщо ми напишемо <імя звязаної моделі>_set.all() то отримаємо
всі дані, які мають цю категорію. Тобто, cat4 = Category.objects.get(pk=4) і cat4.news_set.all()
дасть нам всі дані з такою категорією

<імя поля>__<фільтр> - Синтаксис фільтрів полів

News.objects.filter(pk__gt=12) - Виведе всі pk, значення яких буде більше 12. GT - Greater than

News.objects.filter(pk__gte=12) - Робить то ж саме, але замість > ставить >=, тобто Greater than equal

News.objects.filter(lt__gt=12) - Те ж саме, тільки виводить менше числа, gte зробить <=

News.objects.filter(title__contains='беб')
contains - залежить від регістра
icontains - не залежить від регістра
В sqlite латиниця шукається без зазначення регістра, а кирилиця з регістром, що один фільтр, що інший

in - шукає щось, що рівне певним значенням
News.objects.filter(pk__in=[2, 3, 5])

Фільтри можна комбінувати, приклад знизу
News.objects.filter(pk__in=[2, 3, 5], title__contains='4')

News.objects.first() - виведе першу новину, в залежності від того, як вони відсортовані
News.objects.order_by('pk').first() - комбінуємо сортування і first
Можна використовувати не для всіх записів моделі, а для вже відфільтрованих наборів

News.objects.last() - те ж саме, що first, тільки навпаки

News.objects.earliest('updated_at') - виводить запис, що створений найраніше

News.objects.latest('updated_at') - те ж саме, але виводить найсвіжішу

cat1.news_set.exists() - перевіряє, чи є записи в певній категорії

cat1.news_set.count() - рахує кількість записів з певною категорією

news.get_previous_by_created_at() - повертає попередній запис відносно нашого, використовується тільки, якщо є поле з датою

news.get_next_by_created_at() - те ж саме, що і попереднє, тільки повертає наступну новину
Також можна додавати параметри, наприклад news.get_next_by_created_at(pk__gt=4, title__contains='Гімно')
Тобто нам дадуть наступну новину, pk якої більше 4 і title має в собі слово 'Гімно'

News.objects.filter(category__title='Політика') - означає, що ми отримаємо записи через зовнішній ключ, який у нас
називається category і через назву поля в первинній моделі

Category.objects.filter(news__title__contains='Кака') - в моделі Category отримуємо всі записи, де в title є Кака
І отримуємо їхню категорію

distinct() - видає тільки унікальні значення

В класі Q, який ми імпортуємо з django.db.models, ми можемо використовувати оператори | & ~(Заперечення)

По дефолту в фільтрі у нас завжди стоїть and

News.objects.filter(Q(pk__in=[7]) | Q(title__contains='nv')) - означає, що ми шукаєм новину, pk якої буде = 7
Або новину, title якої містить nv

News.objects.filter(Q(title__contains=334) &~ Q(title__contains=228)) - Означає, що шукаємо новину, де в тайтлі є 334,
Але немає 228

News.objects.all()[:3] - Покаже перші 3 записи, тут використовуються зрізи, як в Python

News.objects.aggregate(Min('views'), Max('views')) - Приклад агрегатної функції, яка виконує певні дії

News.objects.aggregate(Мінімум=Min('views'),Максимум= Max('views')) - Міняємо вивід, називаємо функції своїми іменами

News.objects.aggregate(Sum('views')) - Додає всі значення

News.objects.aggregate(Avg('views')) - дає сер.арифметичне

cats = Category.objects.annotate(Count('news')) - Рахуємо скільки записів з кожній категорії. Count`у ми передаємо
звязану модель

Category.objects.annotate(max_views=Max('news__views')) - Шукаємо максимальну кількість переглядів в кожній категорії

cats = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0) - Шукаємо тільки ті категорії, де кількість записів > 0

News.objects.aggregate(cnt=Count('views', distinct=True)) - Параметр distinct рахує тільки унікальні хначення

news1 = News.objects.values('title', 'views').get(pk=1) - Values дозволяє отримати тільки певні поля даних

news = News.objects.values('title', 'views', 'category__title') - Через звязане поле отримуємо назву

news.views = F('views') + 1 - Додаємо один перегляд до новини
F - спеціальний клас, який треба імпортувати, як і Q

News.objects.filter(content__icontains=F('title')) - Знаходимо запис, де в описі міститься назва title

news = News.objects.annotate(length=Length('title')).all() - Є такі функції, як наприклад Length, які виконують
обчислення на стороні сервера, а не Django. В цьому прикладі ми обрахували кількітсь символів в кожному title`і

News.objects.raw('SELECT * FROM news_news') - функція raw() дозволяє не використовувати ORM, а писати запити на SQL
При використанні raw обовязково треба вибирати з таблицю первинний ключ

news = News.objects.raw("SELECT * FROM news_news WHERE title = %s", ['Гімно моча']) - Якщо ми шукаємо щось за певним
значенням, то треба використовувати %s і тд