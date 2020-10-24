from django.db import models
import datetime

STATUS = [
    ('Не проверен', 'Не проверен'),
    ('Проверен', 'Проверен'),
]


class Question(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return f'{self.question}'


class Calling(models.Model):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.full_name} {self.phone}'


class Tag(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField()

    def __str__(self):
        return f'{self.name}, {self.desc}'


class Category(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField()
    banner = models.ImageField(upload_to='banners')
    banner_alt = models.CharField(max_length=255, default="фото")

    def __str__(self):
        return f'{self.name}, {self.desc}'


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}: {self.category.name}'


class Property(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING, null=True)
    desc = models.TextField()
    desc_short = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}: subcategory - {self.subcategory.name}'


class ProductComment(models.Model):
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()
    rate = models.IntegerField(default=0)
    user_name = models.CharField(max_length=255, default='')
    phone_number = models.CharField(max_length=255, default='')
    pub_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f'{self.prod.name}'


class ProductPhoto(models.Model):
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='video')
    alt = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.prod.name}: alt: {self.alt}, video url - {self.img.url}'


class ProductVideo(models.Model):
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    video = models.FileField(upload_to='video')
    alt = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.prod.name}: alt: {self.alt}, video url - {self.video.url}'


class ProductChar(models.Model):
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    sold = models.IntegerField()
    amount = models.IntegerField()
    props = models.ManyToManyField(Property, through='ProdVal')

    def __str__(self):
        return f'prod - {self.prod.name}, price - {self.price}, sold - {self.sold}, amount - {self.amount}'


class ProdVal(models.Model):
    value = models.CharField(max_length=255)
    prop = models.ForeignKey(Property, on_delete=models.CASCADE)
    prod_char = models.ForeignKey(ProductChar, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.prod_char.prod.name}: {self.prop.name} - {self.value}'


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
        return f"Название товара: {self.product.product.name}"


class Article(models.Model):
    title = models.CharField(max_length=200, help_text="(максимальное число символов: 200)",
                             verbose_name="Название статьи ")

    text = models.TextField(help_text="(максимальное число символов: неограниченно)",
                            verbose_name="Контент статьи ")

    img = models.ImageField(upload_to='media/photos', default='static/Shop/images/default.png', blank=True,
                            help_text="(желательно 250Х250px)",
                            verbose_name="Загрузка картинки")
    pub_date = models.DateTimeField(verbose_name="Дата", auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"


class SiteProfile(models.Model):
    page_name = models.CharField(max_length=50, help_text="(максимальное число символов: 50)",
                                 verbose_name="Название страницы ")
    page_icon = models.ImageField(upload_to='media/photos', default='static/Shop/images/default.png',
                                  help_text="(видна в закладках)",
                                  verbose_name="Иконка страницы ")

    main_logo = models.ImageField(upload_to='media/photos', default='static/Shop/images/default.png',
                                  help_text="(виден на главном меню)",
                                  verbose_name="Логотип страницы ")

    home_slider_video = models.FileField(upload_to='media/videos', default='static/Shop/videos/home_slider_video.mp4',
                                         help_text="(желателено соотношение 8:6)",
                                         verbose_name="Видео на главной странице ")

    phone_number = models.CharField(max_length=20, blank=True,
                                    help_text="(максимальное число символов: 20)",
                                    verbose_name="Телефон в контактах ")
    instagram = models.CharField(max_length=50, blank=True,
                                 help_text="(максимальное число символов: 50)",
                                 verbose_name="Ссылка на Instagramm ")
    whatsup = models.CharField(max_length=50, blank=True,
                               help_text="(максимальное число символов: 50)",
                               verbose_name="Ссылка на Whats'Up ")
    telegram = models.CharField(max_length=50, blank=True,
                                help_text="(максимальное число символов: 50)",
                                verbose_name="Ссылка на Telegram ")
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
        return f"{self.name} - {self.address} - {self.phone} - {self.checked} - {self.pub_date}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderPosition(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductChar, on_delete=models.DO_NOTHING, blank=True, null=True, default=None)
    amount = models.IntegerField(default=1, verbose_name="Заказано")

    def __str__(self):
        return f"{self.product.prod.name}"


class AboutItem(models.Model):
    text = models.TextField(help_text="(максимальное число символов: неограниченно)",
                            verbose_name="Контент статьи ")

    img = models.ImageField(upload_to='media/photos', default='static/Shop/images/default.png', blank=True,
                            help_text="(желательно 250Х250px)",
                            verbose_name="Загрузка картинки")

    def __str__(self):
        return f"Item"

