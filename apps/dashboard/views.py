# Imports
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Dashboard Home View
@login_required
def home_view(request):
    """Dashboard Home View

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """

    # Create a context dictionary
    context = {"user": request.user}

    # Render the dashboard.html template
    return render(request, "dashboard/dashboard.html", context)
