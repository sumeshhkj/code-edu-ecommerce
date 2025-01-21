from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from storeapp.forms import CustomUserForm

def register(request):
    form = CustomUserForm()
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registered Successfully! Login to Continue!")
            return redirect('/login')
    # Ensure the form is passed in both GET and POST cases with errors (if any)
    context = {'form': form}
    return render(request, "store/auth/register.html", context)


def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")
        return redirect("/")

    if request.method == "POST":
        # Fetch form data
        name = request.POST.get("Username")
        passwd = request.POST.get("Password")  # Ensure field name matches login.html

        # Authenticate user
        user = authenticate(request, username=name, password=passwd)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in Successfully!")
            return redirect("/")
        else:
            messages.error(request, "Invalid username or password.")
            # Render the login page again with error message
            return render(request, "store/auth/login.html", {"username": name})

    # Render login page for GET requests or other methods
    return render(request, "store/auth/login.html")
def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out Successfully...!")
    return redirect('/')
