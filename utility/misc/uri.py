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

import base64


class URI(object):
    @staticmethod
    def generic(protocol, host, location, arguments=None):
        return '{PROTOCOL}://{HOST}/{LOCATION}{QUESTION}{ARGUMENTS}'.format(
            PROTOCOL=protocol,
            HOST=host,
            LOCATION=location,
            QUESTION='?' if arguments else '',
            ARGUMENTS=arguments)

    @staticmethod
    def otpauth_totp(secret, account, issuer):
        secret_encoded = base64.b32encode(secret.encode()).decode('utf-8')
        return URI.generic(protocol='otpauth',
                           host='totp',
                           location='{ISSUER}:{ACCOUNT}'.format(
                               ISSUER=issuer, ACCOUNT=account),
                           arguments='secret={SECRET}&issuer={ISSUER}'.format(
                               SECRET=secret_encoded, ISSUER=issuer))
