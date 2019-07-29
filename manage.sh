#!/usr/bin/env bash
##
#     Project: Django Hotels
# Description: A Django application to organize Hotels and Inns
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2018-2019 Fabio Castelli
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

case $1 in
  run)
    python manage.py runserver 0.0.0.0:8000
    ;;
  development)
    python manage.py runserver --settings project.settings_development 0.0.0.0:8000
    ;;
  migrations)
    python manage.py makemigrations --settings project.settings_development
    ;;
  showmigrations)
    python manage.py showmigrations --settings project.settings_development
    ;;
  migrate)
    python manage.py migrate --settings project.settings_development
    ;;
  rollback)
    shift
    python manage.py migrate --settings project.settings_development $*
    ;;
  shell)
    shift
    python manage.py shell --settings project.settings_development $*
    ;;
  *)
    echo "Usage: $0 <run|makemigrations|migrate|migrate>"
    echo "  run             will run the development server using default settings"
    echo "  development     will run the development server using the development settings"
    echo "  migrations      will create the migrations files"
    echo "  showmigrations  will create the migrations files"
    echo "  migrate         will run the migrations"
    echo "  rollback        rollback a migration file"
    echo "                  $0 rollback application migration_file"
    exit 1
    ;;
esac
