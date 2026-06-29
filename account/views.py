from django.shortcuts import render, redirect
from django.views import View
from .forms import UserUpdateForm
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from store.forms import ProductForm
from store.models import Product
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator

def home(request):
    return render(request, 'home.html')



@login_required()
def logout_view(request):
    logout(request)
    return redirect('home')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        products_list = Product.objects.filter(owner=user)
        paginator = Paginator(products_list, 5)
        page_num = request.GET.get('page')
        products = paginator.get_page(page_num)
        return render(request, 'profile.html', {'user': user, 'products': products})




class ChangePasswordView(LoginRequiredMixin, View):
    def post(self, request):
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        if not user.check_password(old_password):
            messages.error(request, "Eski parol noto'g'ri!")
            return redirect('profile')

        if new_password != confirm_password:
            messages.error(request, "Yangi parollar mos kelmadi!")
            return redirect('profile')

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Parol muvaffaqiyatli yangilandi!")
        return redirect('profile')

class UserUpdateView(View):
    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, 'update.html', {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, 'update.html', {'form': form})






class AddProductView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProductForm()
        return render(request, 'add_product.html', {'form': form})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.is_available = True
            product.slug = slugify(form.cleaned_data['name'])
            product.save()
            return redirect('profile')
        return render(request, 'add_product.html', {'form': form})


from django.contrib.auth.views import LoginView
from .forms import SignupForm


class UserLoginView(LoginView):
    template_name = "accounts/login.html"


def signup(request):

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.set_password(form.cleaned_data['password'])
            user.is_active = True

            user.save()

            login(request, user)

            return redirect('/')

    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})
