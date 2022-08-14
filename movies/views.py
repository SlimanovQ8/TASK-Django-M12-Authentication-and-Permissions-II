from django.contrib.auth import login, logout
from django.db import OperationalError
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from movies import forms, models
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
def get_movies(request: HttpRequest) -> HttpResponse:
    try:
        movies: list[models.Movie] = list(models.Movie.objects.all())
    except OperationalError:
        movies = []

    context = {
        "movies": movies,
    }
    return render(request, "movie_list.html", context)


def get_movie(request: HttpRequest, movie_id: int) -> HttpResponse:
    try:
        movie: models.Movie = models.Movie.objects.get(id=movie_id)
    except (OperationalError, models.Movie.DoesNotExist):
        raise Http404(f"no movie found matching {movie_id}")

    context = {
        "movie": movie,
    }
    return render(request, "movie_detail.html", context)

def create_movie(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect("login")
    form = forms.MovieForm()
    if request.method == "POST":
        # BONUS: This needs to have the `user` injected in the constructor
        # somehow
        form = forms.MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {
        "form": form,
    }

    return render(request, "create_movie.html", context)

def register_user(request):
    print("hi")
    form = forms.Registerform()
    print(form)
    if request. method == "POST":
        form = forms.Registerform(request.POST)
        if form.is_valid():
            user = form.save(commit= False)
            user.set_password(user. password)
            user.save()
            login(request, user)
            return redirect("home")
    context = {
        "form": form,
    }
    return render(request, "register.html", context)

def user_login(request):
    form = forms.UserLogin()
    if request.method == "POST":
        form = forms.UserLogin(request.POST)
        if form.is_valid():

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                # Where you want to go after a successful login
                return redirect("home")

    context = {
        "form": form,
    }
    return render(request, "login.html", context)
def logout_view(request):
    logout(request)
    return redirect("home")