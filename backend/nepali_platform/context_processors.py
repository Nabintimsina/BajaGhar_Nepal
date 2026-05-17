from catalog.models import Branding
from catalog.serializers import get_requested_language


def admin_branding(request):
    branding = Branding.objects.filter(pk=1).first()
    language = get_requested_language({'request': request})

    if branding and branding.logo:
        logo_url = branding.logo.url
        name = branding.name_ne if language == 'ne' and branding.name_ne else branding.name or 'BAJAGHAR'
        logo_alt = branding.logo_alt_ne if language == 'ne' and branding.logo_alt_ne else branding.logo_alt or f'{name} logo'
    else:
        logo_url = '/favicon.svg'
        name = 'बाजाघर' if language == 'ne' else 'BAJAGHAR'
        logo_alt = 'बाजाघर लोगो' if language == 'ne' else 'BAJAGHAR logo'

    return {
        'admin_branding_name': name,
        'admin_branding_logo_url': logo_url,
        'admin_branding_logo_alt': logo_alt,
    }