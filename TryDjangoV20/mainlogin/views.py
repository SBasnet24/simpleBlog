from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserLoginForm, UserRegestrationForm, UserUpdateForm, GenericUserRegestrationForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status

def login_view(request):
    if request.user.is_authenticated:
        # return HttpResponseRedirect("/home/")
        return HttpResponseRedirect(reverse("loginapp:home"))

    form = UserLoginForm(request.POST or None)
    title = "Login"
    context = {"form": form, "title": title}
    if form.is_valid():
        username = form.cleaned_data.get("username", "")
        password = form.cleaned_data.get("password", "")
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if "next" in request.POST:
                    return HttpResponseRedirect(request.POST.get("next"))
                # return HttpResponseRedirect("/home/")
                return HttpResponseRedirect(reverse("loginapp:home"))

            else:
                return HttpResponse("User is not activated.")
        else:
            # return HttpResponseRedirect(settings.LOGIN_URL)
            return HttpResponseRedirect(reverse("loginapp:login"))
    return render(request, "mainlogin/form.html", context)



def logout_view(request):
    current_user = request.user
    logout(request)
    print(request.user)
    print("{} has been logged out.".format(current_user))
    # return HttpResponseRedirect("/")
    return HttpResponseRedirect(reverse("loginapp:main"))


@login_required(login_url="/login/")
def register_view(request):
    title = "Register"
    form = GenericUserRegestrationForm(request.POST or None)
    context = {"form": form, "title": title}
    if request.user.is_superuser:
        if form.is_valid():  # runs only if the method is post
            user = form.save(commit=False)
            password = form.cleaned_data.get("password")
            user.set_password(password)
            user.save()
            # return HttpResponseRedirect("/register/")
            return HttpResponseRedirect(reverse("loginapp:register"))
    else:
        context = {"error": "Only super user can create new users."}
        return render(request, "mainlogin/error.html", context)
    return render(request, "mainlogin/form.html", context)


@login_required(login_url="/login/")
def all_user_view(request):
    if request.user.is_superuser:
        users = User.objects.values("id", "username")
        title = "User list"
        context = {"users": users, "title": title}
        return render(request, "mainlogin/list.html", context)
    else:
        context = {"error": "Only super user has access to see all users."}
        return render(request, "mainlogin/error.html", context)


@login_required(login_url="/login/")
def detail_user_view(request, id):
    context = {}
    user = User.objects.get(id=id)
    context["user"] = user
    return render(request, "mainlogin/detail.html", context)


@login_required(login_url="/login/")
def delete_user_view(request, id):
    selecteduser = User.objects.get(id=id)
    context = {}
    if request.user.is_superuser:
        if not selecteduser.is_superuser:
            if request.method == "POST":
                selecteduser.delete()
                # return HttpResponseRedirect("/users/")
                return HttpResponseRedirect(reverse("loginapp:user_list"))
        else:
            context["error"] = "Cannot delete superuser"
            return render(request, "mainlogin/error.html", context)

        context = {
            "user": selecteduser
        }
        return render(request, "mainlogin/user_delete.html", context)
    else:
        context["error"] = "Only superuser can terminate users"
        return render(request, "mainlogin/error.html", context)


@login_required(login_url="/login/")
def update_user_view(request, id):
    user = User.objects.get(id=id)
    title = "Update form"
    if request.user.is_superuser:
        if request.method == 'POST':
            form = UserUpdateForm(request.POST, instance=user)
            update = form.save(commit=False)
            update.save()
            # return HttpResponseRedirect("/users/")
            return HttpResponseRedirect(reverse("loginapp:user_list"))
        else:
            form = UserUpdateForm(instance=user)
            context = {"form": form, "title": title}

        return render(request, 'mainlogin/form.html', context)
    else:
        context = {"error": "Not authorized to perform updates"}
        return render(request, 'mainlogin/error.html', context)

# todo add a password change function and implement it accross the app
