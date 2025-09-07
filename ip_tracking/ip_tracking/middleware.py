from .models import RequestLog

class IPLoggingMiddleware:
    """
    Middleware to log the IP address, timestamp, and path of every
    incoming request to the database.
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

        # Create a log entry in the database.
        if ip_address:
            RequestLog.objects.create(
                ip_address=ip_address,
                path=request.path
            )

        # Process the request and get the response.
        response = self.get_response(request)

        return response
