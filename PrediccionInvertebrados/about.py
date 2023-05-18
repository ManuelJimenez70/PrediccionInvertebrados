import os
from django.http import HttpResponse
from django.template import Context, Template

from PrediccionInvertebrados.settings import BASE_DIR
## tiempo que se tarda en predecir

def about(request):
    prediction = True
    doc = open((os.path.join(BASE_DIR, "PrediccionInvertebrados/templates/about.html")))
    template = Template(doc.read())
    doc.close()
    context = Context()
    document = template.render(context)
    return HttpResponse(document)

