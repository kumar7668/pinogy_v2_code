import logging
from django.utils.translation import activate, deactivate
from django.contrib.sites.models import Site
from django.conf import settings
from cms.models import Title
from cms.sitemaps import CMSSitemap

from pos_api.pos_client import PWAPI

logger = logging.getLogger("debug_logger")

def get_page_data(site=None, languages=None):
    """
    Generate a page data for static and apphook pages.
    """
    if site is None:
        site = Site.objects.get_current()
    if languages is None:
        from django.conf import settings
        languages = settings.LANGUAGES

    # Get all publicly accessible titles for the specified site
    cms_titles = Title.objects.public().filter(
        language__in=[lang[0] for lang in languages],
        page__login_required=False,
        page__node__site=site,
    ).order_by("page__node__path")

    cms_sitemap = CMSSitemap()
    pages_data = []

    for title in cms_titles:
        page = title.page

        # Check if the page has an Apphook
        apphook = page.application_urls

        # Activate the correct language context for generating the URL path
        activate(title.language)
        path = cms_sitemap.location(title)
        deactivate()

        # Determine the kind of page
        if apphook:
            kind = f"apphook.{apphook}"  # Apphook page
        else:
            kind = f"static.{title.slug}"  # Static page with page title

        # Add the page data to the pages list
        page_data = {
            "url": path,
            "kind": kind,
            "contents": {
                # Added the page ID here
                "id": page.id,
                "title": title.title,
                "lastmod": cms_sitemap.lastmod(title).strftime('%Y-%m-%d') if cms_sitemap.lastmod(title) else None,
                "changefreq": "monthly",  # Adjust according to your needs
                "priority": 0.5  # Adjust according to your needs
            },
        }
        pages_data.append(page_data)

    return {"pages": pages_data}

def send_page_data_to_api():
    """
    Common function to send page data to the API.
    """
    logger.info(
        "send_page_data_to_api() called. "
        f"IS_LOCAL: {getattr(settings, 'IS_LOCAL', False)}, "
        f"DEBUG: {settings.DEBUG}"
    )
    if getattr(settings, 'IS_LOCAL', False):
        return

    if not settings.DEBUG:
        return

    site = Site.objects.get_current()
    page_data = get_page_data(site=site)

    logger.info("Sending page data to API: %s", page_data)

    client = PWAPI()
    client.send_page_data(page_data)
