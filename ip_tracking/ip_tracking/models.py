import datetime
from celery import shared_task
from django.db.models import Count
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_anomalies():
    """
    Celery task to detect suspicious IPs based on high request volume
    or access to sensitive paths.
    
    This task should be scheduled to run periodically (e.g., hourly).
    """
    one_hour_ago = datetime.datetime.now() - datetime.timedelta(hours=1)
    
    # 1. Find IPs with high request volume (more than 100 requests in the last hour)
    high_volume_ips = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago
    ).values('ip_address').annotate(
        request_count=Count('ip_address')
    ).filter(
        request_count__gt=100
    )
    
    for entry in high_volume_ips:
        ip = entry['ip_address']
        SuspiciousIP.objects.get_or_create(
            ip_address=ip,
            defaults={'reason': f"Exceeded request limit (100+) in the last hour with {entry['request_count']} requests."}
        )
        print(f"Flagged high-volume IP: {ip}")
    
    # 2. Find IPs that have accessed sensitive paths in the last hour
    sensitive_paths = ['/admin/', '/login/']
    sensitive_access_ips = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago,
        path__in=sensitive_paths
    ).values('ip_address').distinct()
    
    for entry in sensitive_access_ips:
        ip = entry['ip_address']
        SuspiciousIP.objects.get_or_create(
            ip_address=ip,
            defaults={'reason': "Accessed a sensitive path (e.g., /admin, /login) in the last hour."}
        )
        print(f"Flagged IP for sensitive path access: {ip}")
