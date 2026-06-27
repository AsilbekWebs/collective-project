from django.shortcuts import render, get_object_or_404
from cart.views import _cart_id
from cart.models import CartItem
from category.models import Category
from .models import Product
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

def search(request):
    keyword = request.GET.get('keyword')
    products = Product.objects.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))
    context = {
        "products": products,
        "product_count": products.count()
    }
    return render(request, "store.html", context)


def store(request, category_slug=None):
    if category_slug == None:
        products = Product.objects.filter(is_available=True).order_by('id')
    else:
        products = Product.objects.filter(is_available=True, category__slug=category_slug)
    paginator = Paginator(products, 3)
    page_num = request.GET.get('page')
    paged_products = paginator.get_page(page_num)

    context = {
        "products": paged_products,
        "product_count": products.count()
    }
    return render(request, "store.html", context)


# def store(request, category_slug=None):
#     if category_slug == None:
#         products = Product.objects.all()
#     else:
#         categories = get_object_or_404(Category, slug=category_slug)
#         products = Product.objects.filter(is_available=True, category=categories)
#
#
#     context = {'products': products,
#                'products_count':products.count()
#
#     }
#     return render(request, 'store.html', context)


def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    cart_exist = CartItem.objects.filter(cart__session_id=_cart_id(request), product=product).exists()
    context = {
        "product": product,
        "cart_exist": cart_exist
    }

    return render(request, "product-detail.html", context)