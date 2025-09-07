from django.db import models

class RequestLog(models.Model):
    """
    Represents a log of an incoming request, capturing the IP address,
    the time of the request, and the path requested.
    """
    ip_address = models.CharField(max_length=45)
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=2048)

    def __str__(self):
        """
        Returns a string representation of the log entry.
        """
        return f"{self.ip_address} accessed {self.path} at {self.timestamp}"

    class Meta:
        verbose_name = "Request Log"
        verbose_name_plural = "Request Logs"
        ordering = ['-timestamp']
