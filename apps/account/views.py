# Imports
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse

from apps.account.forms import UserLoginForm, UserRegisterForm, UserUpdateForm


# Login view
def login_view(request):
    """Login view

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """

    # Update the form with the request data
    form = UserLoginForm(request.POST or None)

    # If the form is submitted
    if request.method == "POST":
        # If the form is valid
        if form.is_valid():
            # Get the cleaned data
            data = form.cleaned_data

            # Get the email and password
            email = data.get("email")
            password = data.get("password")

            # Authenticate the user
            user = authenticate(email=email, password=password)

            # If the user is authenticated
            if user:
                # Log the user in
                login(request, user)

                # Redirect to the home page
                return redirect(reverse("core:dashboard"))

            # If the user is not authenticated
            else:
                # Add an error message
                messages.error(request, "Invalid email or password")

        # If the form is not valid
        else:
            # Traverse over the form errors
            for field, errors in form.errors.items():
                # Add an error message
                messages.error(
                    request, f"{field.title().replace("_", "")}: {', '.join(errors)}"
                )

    # Create the context
    context = {"form": form}

    # Render the login.html template
    return render(request, "account/login.html", context)


# Logout view
def logout_view(request):
    """Logout view

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """

    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # Add an error message
        messages.error(request, "You are not logged in!")

        # Redirect to the login page
        return redirect(reverse("account:login"))

    # Log the user out
    logout(request)

    # Add a success message
    messages.success(request, "You have been logged out!")

    # Redirect to the login page
    return redirect(reverse("account:login"))


# Register view
def register_view(request):
    """Register view

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """

    # Update the form with the request data
    form = UserRegisterForm(request.POST or None)

    # If the form is submitted
    if request.method == "POST":
        # If the form is valid
        if form.is_valid():
            # Save the form
            form.save()

            # Add a success message
            messages.success(request, "Your account has been created!")

            # Redirect to the login page
            return redirect(reverse("account:login"))

        # If the form is not valid
        else:
            # Traverse over the form errors
            for field, errors in form.errors.items():
                # Add an error message
                messages.error(
                    request, f"{field.title().replace("_", "")}: {', '.join(errors)}"
                )

    # Create the context
    context = {"form": form}

    # Render the register.html template
    return render(request, "account/register.html", context)


# Profile view
@login_required
def profile_view(request):
    """Profile view

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """

    # Get the authenticated user
    user = request.user

    # Update the form with the request data
    form = UserUpdateForm(request.POST or None, request.FILES or None, instance=user)

    # If the form is submitted
    if request.method == "POST":
        # If the form is valid
        if form.is_valid():
            # Create a atomic transaction
            with transaction.atomic():
                # Save the form
                form.save()

            # Add a success message
            messages.success(request, "Your profile has been updated!")

            # Redirect to the profile page
            return redirect(reverse("account:profile"))

        # If the form is not valid
        else:
            # Traverse over the form errors
            for field, errors in form.errors.items():
                # Add an error message
                messages.error(
                    request, f"{field.title().replace("_", "")}: {', '.join(errors)}"
                )

    # Create the context
    context = {"form": form}

    # Render the profile.html template
    return render(request, "account/profile.html", context)
