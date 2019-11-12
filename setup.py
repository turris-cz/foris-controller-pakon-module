#
# foris-controller-pakon-module
# Copyright (C) 2017 CZ.NIC, z.s.p.o. (http://www.nic.cz/)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
#

from setuptools import setup

from foris_controller_pakon_module import __version__

DESCRIPTION = """
Pakon module for foris-controller
"""

setup(
    name='foris-controller-pakon-module',
    version=__version__,
    author='CZ.NIC, z.s.p.o. (http://www.nic.cz/)',
    author_email='stepan.henek@nic.cz',
    packages=[
        'foris_controller_pakon_module',
        'foris_controller_backends',
        'foris_controller_backends.pakon',
        'foris_controller_modules',
        'foris_controller_modules.pakon',
        'foris_controller_modules.pakon.handlers',
    ],
    package_data={
        'foris_controller_modules.pakon': ['schema', 'schema/*.json'],
    },
    namespace_packages=[
        'foris_controller_modules',
        'foris_controller_backends',
    ],
    description=DESCRIPTION,
    long_description=open('README.rst').read(),
    install_requires=[
        "foris-controller @ git+https://gitlab.labs.nic.cz/turris/foris-controller/foris-controller.git#egg=foris-controller",
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'foris-controller-testtools',
        'foris-client',
        'ubus',
        'paho-mqtt',
    ],
    dependency_links=[
        "git+https://gitlab.labs.nic.cz/turris/foris-controller/foris-controller-testtools.git#egg=foris-controller-testtools",
        "git+https://gitlab.labs.nic.cz/turris/foris-controller/foris-client.git#egg=foris-client",
    ],
    include_package_data=True,
    zip_safe=False,
)
