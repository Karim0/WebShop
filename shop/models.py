from django.db import models
import datetime

STATUS = [
    ('Не проверен', 'Не проверен'),
    ('Проверен', 'Проверен'),
    ('Оплачен', 'Оплачен'),
    ('Отклонён', 'Отклонён')
]


class Question(models.Model):
    question = models.CharField(max_length=255, help_text="(максимальное число символов: 255)",
                                verbose_name="Вопрос ")
    answer = models.TextField(verbose_name="Ответ ")

    def __str__(self):
        return f'Вопрос: {self.question}'

    class Meta:
        verbose_name = "Частый вопрос"
        verbose_name_plural = "Частые вопросы"


class Calling(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Вопрос клиента")
    phone = models.CharField(max_length=50, verbose_name="Номер телефона клиента")

    def __str__(self):
        return f'имя: {self.full_name}  телефон: {self.phone}'

    class Meta:
        verbose_name = "Заявка на обратную связь"
        verbose_name_plural = "Заявки на обратную связь"


class Tag(models.Model):
    name = models.CharField(max_length=255, help_text="(максимальное число символов: 255)",
                            verbose_name="Название тэга ")
    desc = models.TextField(verbose_name="Описание тэга ", help_text="необязательно, только для вас",
                            default="Не указан")

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"


class Category(models.Model):
    name = models.CharField(max_length=255, help_text="(максимальное число символов: 255)",
                            verbose_name="Название категории ")
    desc = models.TextField(verbose_name="Описание категории ", help_text="необязательно, только для вас",
                            default="Не указан")
    banner = models.ImageField(help_text="(соотношение 2.39:1 или любой широкоформатный)",
                               verbose_name="Главное фото на странице категории ", upload_to='media/category_banners')

    banner_alt = models.CharField(max_length=255, help_text="(необязательно, нужен только для сео)",
                                  verbose_name="Название фотографии для ALT",
                                  default="Главное фото категории")

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Выбор категории ")
    name = models.CharField(max_length=255, help_text="(максимальное число символов: 255)",
                            verbose_name="Название подкатегории ")

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Под категория"
        verbose_name_plural = "Под категории"


class Property(models.Model):
    name = models.CharField(max_length=255, help_text="(максимальное число символов: 255)",
                            verbose_name="Название фильтра ")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Фильтр"
        verbose_name_plural = "Фильтры"


class Product(models.Model):
    name = models.CharField(max_length=255, help_text="(максимальное число символов: 255)",
                            verbose_name="Название товара ")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE,
                                    verbose_name="Выбор подкатегории ")
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING, null=True,
                            verbose_name="Выбор тэга ", blank=True)
    desc = models.TextField(verbose_name="Полное описание товара ")

    desc_short = models.CharField(max_length=255, help_text="(максимальное число символов: 255)",
                                  verbose_name="Короткое описание товара ")

    def __str__(self):
        return f'Название: {self.name} Подкатегория: {self.subcategory.name}'

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductComment(models.Model):
    prod = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Название товара ")
    text = models.TextField(verbose_name="Текст комментария ")
    rate = models.IntegerField(default=0, help_text="от 0 до 5",
                               verbose_name="Оценка ")
    user_name = models.CharField(max_length=255,
                                 verbose_name="ФИО комментатора")
    phone_number = models.CharField(max_length=255,
                                    verbose_name="Телефон комментатора ")
    pub_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f'ФИО: {self.prod.name} Оценка: {self.rate} Телефон: {self.phone_number} Дата: {self.pub_date}'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class ProductPhoto(models.Model):
    prod = models.ForeignKey(Product, on_delete=models.CASCADE,
                             verbose_name="Выбор товара ")
    img = models.ImageField(upload_to='media/product_photos',
                            help_text="(соотношение 1:1 или вертикальный прямоугольник, ВАЖНО: первая картинка будет видна на карте товара, остальные только на странице товара)",
                            verbose_name="Фотография товара ")
    alt = models.CharField(max_length=255, help_text="(необязательно, нужен только для сео)",
                           verbose_name="Название фотографии для ALT",
                           default="Фото товара")

    def __str__(self):
        return f'Товар: {self.prod.name}  ALT: {self.alt}'

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фотографии"


class ProductVideo(models.Model):
    prod = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Выбор товара ")
    video = models.FileField(upload_to='media/video', help_text="(видео для страницы товара)",
                             verbose_name="Видео о товаре ")
    alt = models.CharField(max_length=255, help_text="(необязательно, нужен только для сео)",
                           verbose_name="Название видео для ALT",
                           default="Видео о товаре")

    def __str__(self):
        return f'Товар: {self.prod.name}  ALT: {self.alt}'

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"


class ProductChar(models.Model):
    prod = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Выбор товара ")
    price = models.IntegerField(verbose_name="Цена товара",
                                default=10000)
    sold = models.IntegerField(default=0, editable=False)
    amount = models.IntegerField(default=0, help_text="(необязательно, только для вас)",
                                 verbose_name="Количество товара")
    props = models.ManyToManyField(Property, through='ProdVal',
                                   verbose_name="Выбор фильтра(ов) ")

    def __str__(self):
        return f'Товар: {self.prod.name} Цена: {self.price} Продано: {self.sold} Осталось: {self.amount}'

    class Meta:
        verbose_name = "Опция товара"
        verbose_name_plural = "Опции товаров"


class ProdVal(models.Model):
    value = models.CharField(max_length=255, help_text="(максимальное число символов: 255)",
                             verbose_name="Значение ")
    prop = models.ForeignKey(Property, on_delete=models.CASCADE,
                             verbose_name="Выбор фильтра ")
    prod_char = models.ForeignKey(ProductChar, on_delete=models.CASCADE, verbose_name="Выбор товара ")

    def __str__(self):
        return f'{self.prop.name} - {self.value}'

    class Meta:
        verbose_name = "Значение"
        verbose_name_plural = "Значения"


class Cart(models.Model):
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None, editable=False)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True, default=None)
    product = models.ForeignKey(ProductChar, on_delete=models.CASCADE, blank=True, null=True, default=None)
    amount = models.IntegerField(default=1, verbose_name="Заказано")

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"

    def __str__(self):
        return f"{self.product.prod.name}"


class Article(models.Model):
    title = models.CharField(max_length=255, help_text="(максимальное число символов: 255)",
                             verbose_name="Название статьи ")

    text = models.TextField(help_text="(максимальное число символов: неограниченно)",
                            verbose_name="Контент статьи ")

    img = models.ImageField(upload_to='media/photos', blank=True,
                            help_text="(соотношение 1:1 или вертикальный прямоугольник, ВАЖНО: первая картинка будет видна на карте товара, остальные только на странице товара)",
                            verbose_name="Загрузка картинки")
    pub_date = models.DateTimeField(verbose_name="Дата", auto_now_add=True, blank=True)

    def __str__(self):
        return f"Название: {self.title} Дата публикации: {self.pub_date}"

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"


class SiteProfile(models.Model):
    page_name = models.CharField(max_length=255, help_text="(максимальное число символов: 255)",
                                 verbose_name="Название страницы ")

    page_icon = models.ImageField(upload_to='media/site',
                                  help_text="(видна на закладках)",
                                  verbose_name="Иконка страницы ")

    page_desc = models.TextField(help_text="(необязательно, нужен только для сео)",
                                 default="Крутой магазин корейской продукции",
                                 verbose_name="Описание страницы в head ")

    main_logo = models.ImageField(upload_to='media/site',
                                  help_text="(виден на главном меню)",
                                  verbose_name="Логотип страницы ")

    home_banner = models.ImageField(upload_to='media/site',
                                    null=True,
                                    help_text="(желателено соотношение 16:9 FULL HD)",
                                    verbose_name="Главный баннер ")

    home_banner_alt = models.CharField(max_length=255, help_text="(необязательно, нужен только для сео)",
                                       verbose_name="Название главного баннера для ALT ",
                                       default="Главный баннер")

    slogan = models.CharField(max_length=255,
                              help_text="(ВАЖНО: слова писать через запятую и пробел, пример: слово1, слово2, ... )",
                              verbose_name="Слоган на главной странице ",
                              default="Очень, крутой, магазин, корейской, продукции")

    phone_number = models.CharField(max_length=20, blank=True,
                                    help_text="(максимальное число символов: 20)",
                                    verbose_name="Телефон в контактах ")
    instagram = models.CharField(max_length=50, blank=True,
                                 help_text="(максимальное число символов: 50)",
                                 verbose_name="Ссылка на Instagram ")
    whatsup = models.CharField(max_length=50, blank=True,
                               help_text="(максимальное число символов: 50)",
                               verbose_name="Ссылка на What's Up ")
    email = models.CharField(max_length=50, blank=True,
                             help_text="(максимальное число символов: 50)",
                             verbose_name="Email адресс ")
    address = models.CharField(max_length=50, blank=True,
                               help_text="(максимальное число символов: 50)",
                               verbose_name="Адресс самовывоза ")
    paylogin = models.CharField(max_length=50, blank=True,
                                help_text="(максимальное число символов: 50)",
                                verbose_name="Платежный логин")

    paypassword = models.CharField(max_length=50, blank=True,
                                   help_text="(максимальное число символов: 50)",
                                   verbose_name="Платежный пароль")

    def __str__(self):
        return f"{self.page_name}"

    class Meta:
        verbose_name = "Профиль сайта"
        verbose_name_plural = "Профили сайта"


class Order(models.Model):
    name = models.CharField(max_length=100, default="Не указан", verbose_name="Имя клиента")
    address = models.CharField(max_length=100, default="Не указан", verbose_name="Адресс клиента")
    email = models.CharField(max_length=100, default="Не указан", verbose_name="Почта")
    phone = models.CharField(max_length=100, default="Не указан", verbose_name="Телефон клиента")
    del_type = models.CharField(max_length=10, default="Не указан", verbose_name="Доставка")
    pay_type = models.CharField(max_length=10, default="Не указан", verbose_name="Оплата")
    total_sum = models.IntegerField(default=0, verbose_name="Общая сумма заказа")
    pub_date = models.DateTimeField(verbose_name="Дата заказа", auto_now_add=True, blank=True)

    checked = models.CharField(
        max_length=20,
        choices=STATUS,
        default='Не проверен',
        verbose_name="Статус заказа"
    )

    def __str__(self):
        return f"ФИО: {self.id} {self.name} Сумма: {self.total_sum} Статус: {self.checked} Дата: {self.pub_date}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderPosition(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=255, default="Не указан", verbose_name="Позиция ")
    amount = models.IntegerField(default=1, verbose_name="Заказано")


    def __str__(self):
        return f"Название: {self.product}  Кол-во: {self.amount}"

    class Meta:
        verbose_name = "Позиция"
        verbose_name_plural = "Позиции"


class AboutItem(models.Model):
    text = models.TextField(help_text="(максимальное число символов: неограниченно)",
                            verbose_name="Контент статьи ")

    img = models.ImageField(upload_to='media/photos', default='static/Shop/images/default.png', blank=True,
                            help_text="(желательно 250Х250px)",
                            verbose_name="Загрузка картинки")

    def __str__(self):
        return f"Описание магазина"

    class Meta:
        verbose_name = "Статья о магазине"
        verbose_name_plural = "Статьи о магазине"
