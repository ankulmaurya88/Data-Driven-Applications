from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout,authenticate, login


from django.contrib.auth import logout as django_logout



def register(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        username = request.POST.get("username")  # Ensure username is retrieved
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not username:  # Ensure username is not empty
            messages.error(request, "Username is required.")
            return redirect("accounts:register")  

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("accounts:register")  

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("accounts:register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("accounts:register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=firstname,
            last_name=lastname,
        )
        user.save()
        print("Account created successfully!")
        messages.success(request, "Account created successfully!")
        return redirect("accounts:login_view")  

        # return redirect("home")
    else:
        return render(request, "account/register.html")



def login_view(request):  
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)  

        if user is not None:
            login(request, user)  
            messages.success(request, "Login successful!")
            return redirect("quizengine:home") 
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("accounts:login_view")
        # return render(request, "account/login.html") 
    else:
        return render(request, "account/login.html")


def logout(request):
    django_logout(request)  
    return redirect("quizengine:home")