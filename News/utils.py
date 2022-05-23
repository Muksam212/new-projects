 # nos ayuda a convertir un html en pdf
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings


from .models import Author
import csv
import os
from xhtml2pdf import pisa
from io import BytesIO


def link_callback(uri, rel):
    sUrl = settings.STATIC_URL
    sRoot = settings.STATIC_ROOT
    mUrl = settings.MEDIA_URL
    mRoot = settings.MEDIA_ROOT

    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl,""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl,""))
    else:
        return uri

    #make sure the file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s'%(sUrl, mUrl)

        )
    return path

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    pisa_status = pisa.CreatePDF(html, link_callback= link_callback,)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type= 'application/pdf')
    return None