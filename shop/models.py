from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField()
    banner = models.ImageField(upload_to='banners/')

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
    desc = models.TextField()
    desc_short = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}: subcategory - {self.subcategory.name}'


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
