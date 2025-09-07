from django.db import models

class RequestLog(models.Model):
    """
    Represents a log of an incoming request, capturing the IP address,
    geolocation data, the time of the request, and the path requested.
    """
    ip_address = models.CharField(max_length=45)
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=2048)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        """
        Returns a string representation of the log entry.
        """
        location = f" from {self.city}, {self.country}" if self.city and self.country else ""
        return f"{self.ip_address}{location} accessed {self.path} at {self.timestamp}"

    class Meta:
        verbose_name = "Request Log"
        verbose_name_plural = "Request Logs"
        ordering = ['-timestamp']

class BlockedIP(models.Model):
    """
    Stores IP addresses that are blocked from accessing the site.
    """
    ip_address = models.GenericIPAddressField(unique=True)

    def __str__(self):
        """
        Returns a string representation of the blocked IP.
        """
        return self.ip_address

    class Meta:
        verbose_name = "Blocked IP"
        verbose_name_plural = "Blocked IPs"

