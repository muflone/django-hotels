from django.views.generic import TemplateView

from ..models import PageSection


class ViewHome(TemplateView):
    """Home view"""
    template_name = 'hotels/home.html'

    def get_context_data(self, **kwargs):
        context = super(ViewHome, self).get_context_data(**kwargs)
        context['request_path'] = self.request.path
        context['home_section'] = PageSection.objects.filter(name='Home')[0]
        context['header_sections'] = PageSection.objects.filter(
            header_order__gt=0).order_by('header_order')
        context['home_sections'] = PageSection.objects.filter(
            home_order__gt=0).order_by('home_order')
        context['page_title'] = context['home_section'].home_title,
        context['page_content'] = context['home_section'].description.replace(
            '\r', '').split('\n\n')
        return context
