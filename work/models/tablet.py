##
#     Project: Django Hotels
# Description: A Django application to organize Hotels and Inns
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2018 Fabio Castelli
#     License: GPL-2+
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
##

import base64
import io
import os.path
import uuid

import pyotp

from django.conf import settings
from django.db import models
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.template import loader
from django.template.response import TemplateResponse
from django.urls import path

from utility.misc import QRCodeImage, URI, get_full_host
from utility.models import BaseModel, BaseModelAdmin


class Tablet(BaseModel):

    description = models.TextField(blank=True)
    status = models.BooleanField(default=True)
    buildings = models.ManyToManyField('hotels.Building',
                                       db_table='work_tablet_buildings',
                                       blank=True)
    guid = models.UUIDField(default=uuid.uuid4, blank=True)

    class Meta:
        # Define the database table
        db_table = 'work_tablet'
        ordering = ['id']
        unique_together = ('guid',)

    def __str__(self):
        return 'Tablet {ID}'.format(ID=self.id)

    def check_password(self, password):
        key = base64.b32encode(self.guid.hex.encode()).decode('utf-8')
        return pyotp.TOTP(key).verify(password, valid_window=1)


class TabletAdmin(BaseModelAdmin):
    readonly_fields = ('id', 'guid', 'qrcode_field', 'autoconfiguration_link')
    change_form_template = 'work/admin_tablet_change.html'
    QRCODE_SIZE = 256

    def photo_thumbnail(self, instance):
        return self.detail_photo_image(instance, 48, 48)

    def get_fields(self, request, obj=None):
        """Reorder the fields list"""
        fields = super().get_fields(request, obj)
        fields = ['id'] + [k for k in fields if k not in 'id']
        # noinspection PyAttributeOutsideInit
        self.full_host = get_full_host(request)
        return fields

    def _get_qrcode_text(self, instance):
        """Return the QRCode text for the instance"""
        return URI.otpauth_totp(secret=instance.guid.hex,
                                account=instance,
                                issuer='Django Hotels')

    def save_model(self, request, obj, form, change):
        """Generate QR Code"""
        # Save model data
        super().save_model(request, obj, form, change)
        qrcode = QRCodeImage(data=self._get_qrcode_text(obj),
                             fit=True,
                             size=8,
                             border=1)
        qrcode.save(os.path.join(settings.MEDIA_ROOT,
                                 'tablets',
                                 '{GUID}.png'.format(GUID=obj.guid)))

    def get_urls(self):
        urls = [
            path('<int:tablet_id>/qrcode/<str:export_format>', self.qrcode),
        ] + super().get_urls()
        return urls

    def qrcode(self, request, tablet_id, export_format):
        """
        Show QR Code using direct rendering or redirect to cached image
        """
        instance = Tablet.objects.get(pk=tablet_id)
        if export_format == 'raw':
            # Direct result from QR Code render in memory
            stream = io.BytesIO()
            qrcode_data = self._get_qrcode_text(instance)
            qrcode = QRCodeImage(data=qrcode_data, fit=True, size=8, border=1)
            qrcode.save(stream)
            stream.seek(0)
            response = HttpResponse(content=stream, content_type='image/png')
        elif export_format == 'png':
            # Redirection to MEDIA folder image
            response = redirect('{PATH}/{FILENAME}'.format(
                    PATH='{MEDIA}tablets'.format(MEDIA=settings.MEDIA_URL),
                    FILENAME='{GUID}.png'.format(GUID=instance.guid)))
        elif export_format == 'admin':
            # Show the admin template
            tablet = Tablet.objects.get(pk=tablet_id)
            # noinspection PyProtectedMember
            context = dict(
               self.admin_site.each_context(request),
               opts=self.model._meta,
               app_label=self.model._meta.app_label,
               object=tablet,
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
            raise Http404('Unexpected format')
        return response

    def qrcode_field(self, instance):
        return self.qrcode(None, instance.id, 'template')

    def autoconfiguration_link(self, instance):
        """Autoconfiguration link for Hotels app"""
        if instance.id:
            url = ('https://hotels.android.muflone.com/api/v1/configuration/'
                   '?tablet_id={ID}'
                   '&tablet_key={GUID}'
                   '&timezone={TIMEZONE}'
                   '&api_url={ROOT_URL}'.format(ID=instance.id,
                                                GUID=instance.guid.hex,
                                                TIMEZONE=settings.TIME_ZONE,
                                                ROOT_URL=self.full_host))
            return url
        else:
            # Invalid tablet ID
            return ''
