from django.db import models
from django.urls import reverse
from category.models import Category
from django.conf import settings


class Product(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products', null=True,blank=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to = 'photoes/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


    def get_url(self):
        return reverse("product_detail", args=[self.category.slug,self.slug])

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user} → {self.product.name}"


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} → {self.product.name}"

CATEGORY_CHOICES = (
    ("Color", "Color"),
    ("Size", "Size"),
    ("Material", "Material"),
)


class VariationManager(models.Manager):
    # def colors(self):
    #     return super(VariationManager, self).filter(category='Color', is_active=True)
    #
    # def sizes(self):
    #     return super(VariationManager, self).filter(category='Size', is_active=True)

    def all_types(self) -> dict:
        manager = super(VariationManager, self)
        types = [i[0] for i in manager.values_list('category').distinct()]

        result = {}
        for category_name in types:
            result[category_name] = manager.filter(category=category_name, is_active=True)

        return result

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self) -> str:
        return f"{self.product.name} {self.category} {self.value}"