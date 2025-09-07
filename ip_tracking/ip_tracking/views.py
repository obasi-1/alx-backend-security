from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django_ratelimit.decorators import ratelimit
from django_ratelimit.exceptions import RateLimitException

@ratelimit(key='ip', rate='10/m', method='POST', block=True)
@ratelimit(key='ip', rate='5/m', method='GET', block=True)
def login_view(request):
    """
    A view that implements rate limiting.

    - Authenticated users are limited to 10 requests per minute (for a POST request).
    - Anonymous users are limited to 5 requests per minute (for a GET request).
    
    The decorator uses a key of 'ip' to track requests based on the client's
    IP address.
    """
    if request.method == 'POST':
        # This is where your login logic would go
        return HttpResponse("Login attempt successful.")
    else:
        return HttpResponse("This is the login page.")

def rate_limit_error(request, exception):
    """
    A simple view to handle RateLimitException.
    
    This function can be configured in your main urls.py as a handler for
    the exception.
    """
    return HttpResponseForbidden("You have exceeded the rate limit. Please try again later.")

# The following try-except block is a simple way to demonstrate handling the exception
# without needing a separate handler in urls.py.
def login_view_with_exception_handling(request):
    try:
        # Call the rate-limited view
        return login_view(request)
    except RateLimitException:
        return HttpResponseForbidden("You have exceeded the rate limit. Please try again later.")
