from django.shortcuts import render, redirect

from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(
                commit = False
            )

            user.set_password(form.cleaned_data["password"])

            user.save()

            return redirect("login")

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


def login_view(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        error = "Неправильний логін або пароль."

    else:
        error = None

    return render(
        request,
        "accounts/login.html",
        {
            "error": error
        }
    )

def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def profile(request):
    favorites = request.user.favorites.select_related('movie').all()

    watch_history = request.user.watch_history.select_related('movie').all()

    return render(
        request,
        "accounts/profile.html",
        {
            "favorites": favorites,
            "watch_history": watch_history
        }
    )














