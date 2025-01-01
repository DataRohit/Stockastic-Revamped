# Imports
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Indices view
@login_required
def indices_view(request):
    """Indices view

    Args:
        request (HttpRequest): The request object

    Returns:
        HttpResponse: The response object
    """

    # Context dictionary
    context = {"user": request.user}

    # Render the indices.html template
    return render(request, "stock/indices.html", context)
