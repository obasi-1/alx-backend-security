from django.core.management.base import BaseCommand, CommandError
from ip_tracking.models import BlockedIP
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address

class Command(BaseCommand):
    """
    A Django management command to add one or more IP addresses to the blocklist.
    Example usage:
    python manage.py block_ip 192.168.1.1 2001:0db8:85a3:0000:0000:8a2e:0370:7334
    """
    help = 'Adds one or more IP addresses to the blocklist.'

    def add_arguments(self, parser):
        """
        Adds command-line arguments to the command.
        """
        parser.add_argument(
            'ip_addresses',
            metavar='ip_address',
            nargs='+',
            help='An IP address to be blocked.'
        )

    def handle(self, *args, **options):
        """
        The main logic of the command.
        """
        ip_addresses = options['ip_addresses']
        for ip_address in ip_addresses:
            try:
                # Validate if the provided string is a valid IP address (IPv4 or IPv6)
                validate_ipv46_address(ip_address)

                # Use get_or_create to add the IP and avoid duplicates.
                # 'obj' is the BlockedIP instance, 'created' is a boolean.
                obj, created = BlockedIP.objects.get_or_create(ip_address=ip_address)

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully blocked IP: {ip_address}'))
                else:
                    self.stdout.write(self.style.WARNING(f'IP address {ip_address} was already blocked.'))

            except ValidationError:
                raise CommandError(f'"{ip_address}" is not a valid IP address.')
