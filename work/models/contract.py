##
#     Project: Django Hotels
# Description: A Django application to organize Hotels and Inns
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2018-2019 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

import datetime
import io
import os.path
import uuid

from django.conf import settings
from django.db import models
from django.contrib import admin
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.template import loader
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.safestring import mark_safe
from django.utils.translation import pgettext_lazy

from utility.admin import AdminTextInputFilter
from utility.misc import QRCodeImage, URI, xhtml2pdf_render_from_html
from utility.models import BaseModel, BaseModelAdmin

from website.models import AdminOption


class ContractManager(models.Manager):
    def get_active_contracts_query(self):
        """Return a filter for only active contracts"""
        return (models.Q(enabled=True) &
                # Start date less or equal than today
                models.Q(start_date__lte=datetime.date.today()) &
                # End date is missing or after or equal today
                (models.Q(end_date__isnull=True) |
                 models.Q(end_date__gte=datetime.date.today())))


class Contract(BaseModel):
    # Define custom manager
    objects = ContractManager()

    employee = models.ForeignKey('Employee',
                                 on_delete=models.PROTECT,
                                 verbose_name=pgettext_lazy('Contract',
                                                            'employee'))
    company = models.ForeignKey('hotels.Company',
                                on_delete=models.PROTECT,
                                verbose_name=pgettext_lazy('Contract',
                                                           'company'))
    description = models.TextField(blank=True,
                                   verbose_name=pgettext_lazy('Contract',
                                                              'description'))
    contract_type = models.ForeignKey('ContractType',
                                      on_delete=models.PROTECT,
                                      default=0,
                                      verbose_name=pgettext_lazy(
                                          'Contract',
                                          'contract type'))
    job_type = models.ForeignKey('JobType',
                                 on_delete=models.PROTECT,
                                 default=0,
                                 verbose_name=pgettext_lazy('Contract',
                                                            'job type'))
    roll_number = models.CharField(max_length=255,
                                   verbose_name=pgettext_lazy('Contract',
                                                              'roll number'))
    start_date = models.DateField(verbose_name=pgettext_lazy('Contract',
                                                             'start date'))
    end_date = models.DateField(null=True,
                                blank=True,
                                verbose_name=pgettext_lazy('Contract',
                                                           'end date'))
    level = models.PositiveIntegerField(verbose_name=pgettext_lazy('Contract',
                                                                   'level'))
    enabled = models.BooleanField(default=True,
                                  verbose_name=pgettext_lazy('Contract',
                                                             'enabled'))
    associated = models.BooleanField(verbose_name=pgettext_lazy('Contract',
                                                                'associated'))
    guid = models.UUIDField(default=uuid.uuid4,
                            blank=True,
                            verbose_name=pgettext_lazy('Contract',
                                                       'guid'))
    buildings = models.ManyToManyField('hotels.Building',
                                       db_table='work_contract_buildings',
                                       blank=True,
                                       verbose_name=pgettext_lazy('Contract',
                                                                  'buildings'))

    class Meta:
        # Define the database table
        db_table = 'work_contracts'
        ordering = ['company', 'employee', 'end_date']
        unique_together = (('company', 'employee', 'roll_number'),
                           ('company', 'employee', 'start_date', 'end_date'),
                           ('guid', ))
        verbose_name = pgettext_lazy('Contract', 'Contract')
        verbose_name_plural = pgettext_lazy('Contract', 'Contracts')

    def __str__(self):
        return '{COMPANY} - {EMPLOYEE} ({ROLL_NUMBER})'.format(
            COMPANY=self.company,
            EMPLOYEE=self.employee,
            ROLL_NUMBER=self.roll_number)

    def active(self):
        """Return a boolean value to identify currently active contract"""
        today = datetime.date.today()
        # noinspection PyTypeChecker,PyUnresolvedReferences
        return (self.id is not None and
                self.enabled and
                self.start_date <= today and
                (self.end_date is None or self.end_date >= today))
    active.boolean = True
    active.short_description = pgettext_lazy('Contract', 'Active')


class ContractAdminEmployeeRollNumberInputFilter(AdminTextInputFilter):
    parameter_name = 'roll_number'
    title = pgettext_lazy('Contract', 'roll number')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(roll_number=self.value())


class ContractAdminActiveFilter(admin.SimpleListFilter):
    parameter_name = 'active'
    title = pgettext_lazy('Contract', 'active')

    def lookups(self, request, model_admin):
        return (1, pgettext_lazy('Contract', 'Yes')),\
               (0, pgettext_lazy('Contract', 'No'))

    def queryset(self, request, queryset):
        if self.value() is not None:
            if self.value() == '0':
                # Filter items with Active contract
                return queryset.exclude(
                    Contract.objects.get_active_contracts_query())
            elif self.value() == '1':
                # Filter items with not Active contract
                return queryset.filter(
                    Contract.objects.get_active_contracts_query())


class ContractAdmin(BaseModelAdmin):
    readonly_fields = ('id', 'guid', 'qrcode_field', 'active')
    change_form_template = 'work/admin_contract_change.html'
    QRCODE_SIZE = 256

    def first_name(self, instance):
        return instance.employee.first_name
    first_name.short_description = pgettext_lazy('Employee', 'First name')

    def last_name(self, instance):
        return instance.employee.last_name
    last_name.short_description = pgettext_lazy('Employee', 'Last name')

    def detail_photo_image(self, instance, width, height):
        if instance.employee.photo.url.startswith(
                os.path.join(settings.MEDIA_URL, 'standard%3A')):
            iconset = instance.employee.photo.url.split('%3A', 1)[1]
            base_url = os.path.join(settings.STATIC_URL,
                                    'hotels/images/{ICONSET}/'
                                    '{SIZE}x{SIZE}.png')
            url_thumbnail = base_url.format(ICONSET=iconset, SIZE=width)
            url_image = base_url.format(ICONSET=iconset, SIZE=512)
        else:
            # Show image
            url_thumbnail = instance.employee.photo.url
            url_image = url_thumbnail

        return mark_safe('<a href="{url}" target="_blank">'
                         '<img src="{thumbnail}" '
                         'width="{width}" '
                         'height={height} />'.format(url=url_image,
                                                     thumbnail=url_thumbnail,
                                                     width=width,
                                                     height=height))

    def photo_thumbnail(self, instance):
        return self.detail_photo_image(instance, 48, 48)
    photo_thumbnail.short_description = pgettext_lazy('Employee',
                                                      'Photo thumbnail')

    def get_fields(self, request, obj=None):
        """Reorder the fields list"""
        fields = super().get_fields(request, obj)
        fields = ['id', 'active'] + [k for k in fields
                                     if k not in ('id', 'active')]
        return fields

    def save_model(self, request, obj, form, change):
        """Generate QR Code"""
        account_name = obj.employee.first_name
        qrcode = QRCodeImage(data=URI.otpauth_totp(secret=obj.guid.hex,
                                                   account=account_name,
                                                   issuer='Django Hotels'),
                             fit=True,
                             size=8,
                             border=1)
        qrcode.save(os.path.join(settings.MEDIA_ROOT,
                                 'qrcode',
                                 '{GUID}.png'.format(GUID=obj.guid)))
        # Save model data
        super().save_model(request, obj, form, change)

    def get_urls(self):
        urls = [
            path('<int:contract_id>/qrcode/<str:export_format>', self.qrcode),
            path('<int:contract_id>/idcard/', self.idcard),
        ] + super().get_urls()
        return urls

    def qrcode(self, request, contract_id, export_format):
        """
        Show QR Code using direct rendering or redirect to cached image
        """
        instance = Contract.objects.get(pk=contract_id)
        if export_format == 'raw':
            # Direct result from QR Code render in memory
            stream = io.BytesIO()
            account_name = instance.employee.first_name
            qrcode_data = URI.otpauth_totp(secret=instance.guid.hex,
                                           account=account_name,
                                           issuer='Django Hotels')
            qrcode = QRCodeImage(data=qrcode_data, fit=True, size=8, border=1)
            qrcode.save(stream)
            stream.seek(0)
            response = HttpResponse(content=stream, content_type='image/png')
        elif export_format == 'png':
            # Redirection to MEDIA folder image
            response = redirect('{PATH}/{FILENAME}'.format(
                    PATH='{MEDIA}qrcode'.format(MEDIA=settings.MEDIA_URL),
                    FILENAME='{GUID}.png'.format(GUID=instance.guid)))
        elif export_format == 'admin':
            # Show the admin template
            contract = Contract.objects.get(pk=contract_id)
            # noinspection PyProtectedMember,PyProtectedMember
            context = dict(
               self.admin_site.each_context(request),
               opts=self.model._meta,
               app_label=self.model._meta.app_label,
               object=contract,
               FORMAT='png',
               LINK='png',
               TARGET='_blank',
               SIZE=self.QRCODE_SIZE,
            )
            response = TemplateResponse(request,
                                        'work/admin_qrcode.html',
                                        context)
        elif export_format == 'template':
            # Show the QR Code template (used by qrcode_field)
            template = loader.get_template('work/qrcode.html')
            context = {
                'FORMAT': '../qrcode/png',
                'LINK': '../qrcode/admin',
                'TARGET': '',
                'SIZE': self.QRCODE_SIZE,
            }
            response = template.render(context)
        else:
            raise Http404(pgettext_lazy('Contract', 'Unexpected format'))
        return response

    def qrcode_field(self, instance):
        return self.qrcode(None, instance.id, 'template')
    qrcode_field.short_description = pgettext_lazy('Contract', 'QR Code')

    def idcard(self, request, contract_id):
        """
        Create an ID card in PDF format
        """
        contract = Contract.objects.get(pk=contract_id)
        admin_option = AdminOption.objects.get(section=self.__class__.__name__,
                                               name='contract_id_card',
                                               enabled=True)
        html = admin_option.value.format(
            CONTRACT_START_DATE=contract.start_date,
            CONTRACT_GUID=contract.guid,
            EMPLOYEE_FIRST_NAME=contract.employee.first_name,
            EMPLOYEE_LAST_NAME=contract.employee.last_name,
            EMPLOYEE_BIRTH_DATE=contract.employee.birth_date,
            COMPANY_NAME=contract.company.name,
            COMPANY_ADDRESS=contract.company.address,
            COMPANY_VAT_NUMBER=contract.company.vat_number,
            COMPANY_OWNER=contract.company.owner,
            )
        response = xhtml2pdf_render_from_html(
            html=html, filename='id_card {ID}.pdf'.format(ID=contract_id))
        return response
