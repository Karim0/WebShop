# Generated by Django 3.1.2 on 2020-10-25 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_aboutitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aboutitem',
            options={'verbose_name': 'Статья о магазине', 'verbose_name_plural': 'Статьи о магазине'},
        ),
        migrations.AlterModelOptions(
            name='calling',
            options={'verbose_name': 'Заявка на обратную связь', 'verbose_name_plural': 'Заявки на обратную связь'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='orderposition',
            options={'verbose_name': 'Позиция', 'verbose_name_plural': 'Позиции'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.AlterModelOptions(
            name='productchar',
            options={'verbose_name': 'Опция товара', 'verbose_name_plural': 'Опции товаров'},
        ),
        migrations.AlterModelOptions(
            name='productcomment',
            options={'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.AlterModelOptions(
            name='productphoto',
            options={'verbose_name': 'Фото', 'verbose_name_plural': 'Фотографии'},
        ),
        migrations.AlterModelOptions(
            name='productvideo',
            options={'verbose_name': 'Видео', 'verbose_name_plural': 'Видео'},
        ),
        migrations.AlterModelOptions(
            name='prodval',
            options={'verbose_name': 'Значение', 'verbose_name_plural': 'Значения'},
        ),
        migrations.AlterModelOptions(
            name='property',
            options={'verbose_name': 'Фильтр', 'verbose_name_plural': 'Фильтры'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'Частый вопрос', 'verbose_name_plural': 'Частые вопросы'},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'verbose_name': 'Под категория', 'verbose_name_plural': 'Под категории'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Тэг', 'verbose_name_plural': 'Тэги'},
        ),
        migrations.RemoveField(
            model_name='siteprofile',
            name='home_slider_video',
        ),
        migrations.RemoveField(
            model_name='siteprofile',
            name='telegram',
        ),
        migrations.AddField(
            model_name='siteprofile',
            name='home_banner',
            field=models.ImageField(help_text='(желателено соотношение 16:9 FULL HD)', null=True, upload_to='media/site', verbose_name='Главный баннер '),
        ),
        migrations.AddField(
            model_name='siteprofile',
            name='home_banner_alt',
            field=models.CharField(default='Главный баннер', help_text='(необязательно, нужен только для сео)', max_length=255, verbose_name='Название главного баннера для ALT '),
        ),
        migrations.AddField(
            model_name='siteprofile',
            name='page_desc',
            field=models.TextField(default='Крутой магазин корейской продукции', help_text='(необязательно, нужен только для сео)', verbose_name='Описание страницы в head '),
        ),
        migrations.AlterField(
            model_name='article',
            name='img',
            field=models.ImageField(blank=True, help_text='(соотношение 1:1 или вертикальный прямоугольник, ВАЖНО: первая картинка будет видна на карте товара, остальные только на странице товара)', upload_to='media/photos', verbose_name='Загрузка картинки'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(help_text='(максимальное число символов: 255)', max_length=255, verbose_name='Название статьи '),
        ),
        migrations.AlterField(
            model_name='calling',
            name='full_name',
            field=models.CharField(max_length=255, verbose_name='Вопрос клиента'),
        ),
        migrations.AlterField(
            model_name='calling',
            name='phone',
            field=models.CharField(max_length=50, verbose_name='Номер телефона клиента'),
        ),
        migrations.AlterField(
            model_name='category',
            name='banner',
            field=models.ImageField(help_text='(соотношение 2.39:1 или любой широкоформатный)', upload_to='media/category_banners', verbose_name='Главное фото на странице категории '),
        ),
        migrations.AlterField(
            model_name='category',
            name='banner_alt',
            field=models.CharField(default='Главное фото категории', help_text='(необязательно, нужен только для сео)', max_length=255, verbose_name='Название фотографии для ALT'),
        ),
        migrations.AlterField(
            model_name='category',
            name='desc',
            field=models.TextField(default='Не указан', help_text='необязательно, только для вас', verbose_name='Описание категории '),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='(максимальное число символов: 255)', max_length=255, verbose_name='Название категории '),
        ),
        migrations.AlterField(
            model_name='order',
            name='checked',
            field=models.CharField(choices=[('Не проверен', 'Не проверен'), ('Проверен', 'Проверен'), ('Оплачен', 'Оплачен'), ('Отклонён', 'Отклонён')], default='Не проверен', max_length=20, verbose_name='Статус заказа'),
        ),
        migrations.AlterField(
            model_name='product',
            name='desc',
            field=models.TextField(verbose_name='Полное описание товара '),
        ),
        migrations.AlterField(
            model_name='product',
            name='desc_short',
            field=models.CharField(help_text='(максимальное число символов: 255)', max_length=255, verbose_name='Короткое описание товара '),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(help_text='(максимальное число символов: 255)', max_length=255, verbose_name='Название товара '),
        ),
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.subcategory', verbose_name='Выбор подкатегории '),
        ),
        migrations.AlterField(
            model_name='product',
            name='tag',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='shop.tag', verbose_name='Выбор тэга '),
        ),
        migrations.AlterField(
            model_name='productchar',
            name='amount',
            field=models.IntegerField(default=0, help_text='(необязательно, только для вас)', verbose_name='Количество товара'),
        ),
        migrations.AlterField(
            model_name='productchar',
            name='price',
            field=models.IntegerField(default=10000, verbose_name='Цена товара'),
        ),
        migrations.AlterField(
            model_name='productchar',
            name='prod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Выбор товара '),
        ),
        migrations.AlterField(
            model_name='productchar',
            name='props',
            field=models.ManyToManyField(through='shop.ProdVal', to='shop.Property', verbose_name='Выбор фильтра(ов) '),
        ),
        migrations.AlterField(
            model_name='productchar',
            name='sold',
            field=models.IntegerField(default=10000, editable=False),
        ),
        migrations.AlterField(
            model_name='productcomment',
            name='phone_number',
            field=models.CharField(max_length=255, verbose_name='Телефон комментатора '),
        ),
        migrations.AlterField(
            model_name='productcomment',
            name='prod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Название товара '),
        ),
        migrations.AlterField(
            model_name='productcomment',
            name='rate',
            field=models.IntegerField(default=0, help_text='от 0 до 5', verbose_name='Оценка '),
        ),
        migrations.AlterField(
            model_name='productcomment',
            name='text',
            field=models.TextField(verbose_name='Текст комментария '),
        ),
        migrations.AlterField(
            model_name='productcomment',
            name='user_name',
            field=models.CharField(max_length=255, verbose_name='ФИО комментатора'),
        ),
        migrations.AlterField(
            model_name='productphoto',
            name='alt',
            field=models.CharField(default='Фото товара', help_text='(необязательно, нужен только для сео)', max_length=255, verbose_name='Название фотографии для ALT'),
        ),
        migrations.AlterField(
            model_name='productphoto',
            name='img',
            field=models.ImageField(help_text='(соотношение 1:1 или вертикальный прямоугольник, ВАЖНО: первая картинка будет видна на карте товара, остальные только на странице товара)', upload_to='media/product_photos', verbose_name='Фотография товара '),
        ),
        migrations.AlterField(
            model_name='productphoto',
            name='prod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Выбор товара '),
        ),
        migrations.AlterField(
            model_name='productvideo',
            name='alt',
            field=models.CharField(default='Видео о товаре', help_text='(необязательно, нужен только для сео)', max_length=255, verbose_name='Название видео для ALT'),
        ),
        migrations.AlterField(
            model_name='productvideo',
            name='prod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Выбор товара '),
        ),
        migrations.AlterField(
            model_name='productvideo',
            name='video',
            field=models.FileField(help_text='(видео для страницы товара)', upload_to='media/video', verbose_name='Видео о товаре '),
        ),
        migrations.AlterField(
            model_name='prodval',
            name='prod_char',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.productchar', verbose_name='Выбор товара '),
        ),
        migrations.AlterField(
            model_name='prodval',
            name='prop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.property', verbose_name='Выбор фильтра '),
        ),
        migrations.AlterField(
            model_name='prodval',
            name='value',
            field=models.CharField(help_text='(максимальное число символов: 255)', max_length=255, verbose_name='Значение '),
        ),
        migrations.AlterField(
            model_name='property',
            name='name',
            field=models.CharField(help_text='(максимальное число символов: 255)', max_length=255, verbose_name='Название фильтра '),
        ),
        migrations.AlterField(
            model_name='question',
            name='answer',
            field=models.TextField(verbose_name='Ответ '),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.CharField(help_text='(максимальное число символов: 255)', max_length=255, verbose_name='Вопрос '),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='main_logo',
            field=models.ImageField(help_text='(виден на главном меню)', upload_to='media/site', verbose_name='Логотип страницы '),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='page_icon',
            field=models.ImageField(help_text='(видна на закладках)', upload_to='media/site', verbose_name='Иконка страницы '),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='page_name',
            field=models.CharField(help_text='(максимальное число символов: 255)', max_length=255, verbose_name='Название страницы '),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.category', verbose_name='Выбор категории '),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='name',
            field=models.CharField(help_text='(максимальное число символов: 255)', max_length=255, verbose_name='Название подкатегории '),
        ),
        migrations.AlterField(
            model_name='tag',
            name='desc',
            field=models.TextField(default='Не указан', help_text='необязательно, только для вас', verbose_name='Описание тэга '),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(help_text='(максимальное число символов: 255)', max_length=255, verbose_name='Название тэга '),
        ),
    ]
