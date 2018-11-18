from django.shortcuts import render

from .models import PageSection


# Create your views here.
def home(request):
    home_section = PageSection.objects.filter(name='Home')[0]
    header_sections = PageSection.objects.filter(header_order__gt=0)
    home_sections = PageSection.objects.filter(home_order__gt=0)
    return render(request, 'hotels/home.html', {
                    'page_title': home_section.home_title,
                    'page_content': home_section.description.replace(
                        '\r', '').split('\n\n'),
                    'request_path': request.path,
                    'home_section': home_section,
                    'header_sections': header_sections.order_by('header_order'),
                    'home_sections': home_sections.order_by('home_order'),
                  })
