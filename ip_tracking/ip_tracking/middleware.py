from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP

class IPLoggingMiddleware:
    """
    Middleware to log incoming requests and block requests from
    IP addresses found in the BlockedIP list.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the client's IP address.
        # 'HTTP_X_FORWARDED_FOR' is used for proxies, otherwise 'REMOTE_ADDR'.
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        # If an IP address is found, check if it's blocked.
        if ip_address:
            if BlockedIP.objects.filter(ip_address=ip_address).exists():
                return HttpResponseForbidden("<h1>Forbidden</h1><p>Your IP address has been blocked.</p>")

            # If not blocked, log the request.
            RequestLog.objects.create(
                ip_address=ip_address,
                path=request.path
            )

        # Process the request and get the response.
        response = self.get_response(request)

        return response

