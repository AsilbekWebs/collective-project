from django.shortcuts import render, redirect
from django.contrib.auth import login
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