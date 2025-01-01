# Imports
from django.shortcuts import render


# Home view
def home_view(request):
    """Home view

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """

    # Create a context dictionary
    context = {"user": request.user}

    # Render the home.html template
    return render(request, "core/home.html", context)
