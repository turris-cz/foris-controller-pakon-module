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

import logging
import socket

logger = logging.getLogger(__name__)


class PakonException(Exception):
    pass


class PakonSocket(object):

    def __init__(self, socket_path):
        self.socket_path = socket_path

    def __enter__(self):
        logger.debug("Connecting to pakon socket.")
        try:
            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.socket.connect(self.socket_path)
        except socket.error:
            raise PakonException("Failed to connect to socket '%s'." % self.socket_path)

        logger.debug("Connected to pakon socket.")

        return self

    def query(self, data):
        try:
            self.socket.sendall((data + "\n").encode())
            logger.debug("Querying pakon socket.")
            f = self.socket.makefile()
            try:
                response = f.readline().strip()
            finally:
                f.close()
            logger.debug("Response recieved (len=%d)" % len(response))
        except:
            raise PakonException("Failed to perform the query '%s'" % data)

        return response

    def __exit__(self, exc_type, value, traceback):
        self.socket.close()
        logger.debug("Disconnected from pakon")
