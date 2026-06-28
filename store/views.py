from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from cart.views import _cart_id
from cart.models import CartItem
from category.models import Category
from .models import Product, Like, Comment
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProductForm


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


def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    cart_exist = CartItem.objects.filter(cart__session_id=_cart_id(request), product=product).exists()
    comments = product.comments.all().order_by('-created_at')
    like_count = product.likes.count()
    user_liked = False
    if request.user.is_authenticated:
        user_liked = product.likes.filter(user=request.user).exists()

    context = {
        "product": product,
        "cart_exist": cart_exist,
        "comments": comments,
        "like_count": like_count,
        "user_liked": user_liked,
    }
    return render(request, "product-detail.html", context)


class LikeProductView(LoginRequiredMixin, View):
    login_url = 'login'
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        like, created = Like.objects.get_or_create(user=request.user, product=product)
        if not created:
            like.delete()
        return redirect(request.META.get('HTTP_REFERER', 'store'))


class AddCommentView(LoginRequiredMixin, View):
    login_url = 'login'
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        text = request.POST.get('text')
        if text:
            Comment.objects.create(user=request.user, product=product, text=text)
        return redirect(request.META.get('HTTP_REFERER', 'store'))

class EditProductView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, owner=request.user)
        form = ProductForm(instance=product)
        return render(request, 'edit_product.html', {'form': form, 'product': product})

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, owner=request.user)
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, 'edit_product.html', {'form': form, 'product': product})


class DeleteProductView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id, owner=request.user)
        product.delete()
        return redirect('profile')