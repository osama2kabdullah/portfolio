from .models import SiteSettings
from about_me.models import Profile

def site_settings(request):
    try:
        settings = SiteSettings.load()
    except Exception:
        settings = None
    profile = Profile.objects.filter(is_active=True).first()
    social_links = profile.social_links.all() if profile else []
    return {
        "site_settings": settings,
        "social_links": social_links,
    }
