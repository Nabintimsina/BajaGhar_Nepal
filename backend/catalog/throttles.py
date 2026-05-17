"""Custom throttle classes for API rate limiting."""
import time

from django.conf import settings
from django.core.cache import cache
from rest_framework.throttling import BaseThrottle


class ContactFormThrottle(BaseThrottle):
    """
    Rate limit contact form submissions per IP address.
    Prevents spam and abuse of contact form.
    """
    
    def get_client_ip(self, request):
        """Extract client IP from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def _get_cache_key(self, request):
        ip = self.get_client_ip(request) or 'unknown'
        return f'contact_form_{ip}'

    def allow_request(self, request, view):
        """Allow a request until the configured submission limit is reached."""
        rate_limit = getattr(settings, 'CONTACT_FORM_RATE_LIMIT', 3)
        time_window = getattr(settings, 'CONTACT_FORM_TIME_WINDOW', 86400)
        cache_key = self._get_cache_key(request)
        record = cache.get(cache_key)
        now = time.time()

        if not record or record.get('reset_at', 0) <= now:
            cache.set(
                cache_key,
                {
                    'count': 1,
                    'reset_at': now + time_window,
                },
                timeout=time_window,
            )
            self._wait = None
            return True

        if record.get('count', 0) >= rate_limit:
            self._wait = max(1, int(record['reset_at'] - now))
            return False

        record['count'] += 1
        remaining = max(1, int(record['reset_at'] - now))
        cache.set(cache_key, record, timeout=remaining)
        self._wait = None
        return True

    def wait(self):
        return getattr(self, '_wait', None)
