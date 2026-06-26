from django.shortcuts import render, get_object_or_404

from category.models import Category
from .models import Product

# Create your views here.
def store(request, category_slug=None):
    if category_slug == None:
        products = Product.objects.all()
    else:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(is_available=True, category=categories)


    context = {'products': products,
               'products_count':products.count()

    }
    return render(request, 'store.html', context)

def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)
    return render(request, 'product-detail.html', {'product': product})