from django.http import HttpResponseForbidden
from django.core.cache import cache
from .models import RequestLog, BlockedIP

# django-ipgeolocation provides a function to get geolocation data.
# We'll handle the case where the library might not be installed.
try:
    from ip_geolocation.api import get_ip_geolocation
except ImportError:
    get_ip_geolocation = None


class IPLoggingMiddleware:
    """
    Middleware to log requests with geolocation and block blacklisted IPs.
    Geolocation data is cached for 24 hours to reduce API calls.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        if not ip_address:
            return self.get_response(request)

        # Check if the IP is blacklisted
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("<h1>Forbidden</h1><p>Your IP address has been blocked.</p>")

        # Attempt to get geolocation data
        country, city = None, None
        if get_ip_geolocation:
            cache_key = f"geolocation_{ip_address}"
            geolocation_data = cache.get(cache_key)

            if not geolocation_data:
                # If not in cache, fetch from API
                geo_response = get_ip_geolocation(ip_address)
                if geo_response and geo_response.get('status') == 'success':
                    geolocation_data = {
                        'country': geo_response.get('country'),
                        'city': geo_response.get('city'),
                    }
                    # Cache the result for 24 hours (86400 seconds)
                    cache.set(cache_key, geolocation_data, timeout=86400)
            
            if geolocation_data:
                country = geolocation_data.get('country')
                city = geolocation_data.get('city')

        # Log the request with geolocation data
        RequestLog.objects.create(
            ip_address=ip_address,
            path=request.path,
            country=country,
            city=city
        )

        response = self.get_response(request)
        return response

