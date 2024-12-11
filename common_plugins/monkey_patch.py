#FIXME: Remove this monkey patch when we update python version on prod
import mimetypes

from filer.models.abstract import BaseImage

def match_webp(cls, iname, ifile, mime_type):
    # source: https://www.freeformatter.com/mime-types-list.html
    image_subtypes = ['gif', 'jpeg', 'png', 'x-png', 'svg+xml', 'webp']
    maintype, subtype = mime_type.split('/')
    return maintype == 'image' and subtype in image_subtypes

BaseImage.matches_file_type = classmethod(match_webp) # monkey-patching here
mimetypes.add_type("image/webp", ".webp")