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

import os
import json
import multiprocessing
import pytest
import random
import string
import sys


if sys.version_info >= (3, 0):
    from socketserver import BaseRequestHandler, UnixStreamServer, ThreadingMixIn
else:
    from SocketServer import (
        BaseRequestHandler, UnixStreamServer, ThreadingMixIn as NonObjectThreadingMixIn
    )

    class ThreadingMixIn(object, NonObjectThreadingMixIn):
        pass


PAKON_QUERY_SOCK = "/tmp/pakon-query.sock"


class PakonSocketMockHandler(BaseRequestHandler):
    LENGTH = 1024 * 1024  # always return big data

    def handle(self):
        f = self.request.makefile()
        try:
            # just read the response
            f.readline().strip()
        finally:
            f.close()
        data = "".join(random.choice(string.ascii_letters) for _ in range(
            PakonSocketMockHandler.LENGTH))
        self.request.sendall((json.dumps({"result": data}) + "\n").encode())


class MockPakonServer(ThreadingMixIn, UnixStreamServer):

    def __init__(self, socket_path):
        try:
            os.unlink(socket_path)  # remove socket if needed
        except OSError:
            pass
        UnixStreamServer.__init__(self, socket_path, PakonSocketMockHandler)


@pytest.fixture(scope="session")
def mocked_pakon_server():
    os.environ["PAKON_QUERY_SOCK"] = PAKON_QUERY_SOCK

    ready = multiprocessing.Event()
    ready.clear()

    def start_server(socket_path, ready):
        server = MockPakonServer(socket_path)
        ready.set()
        server.serve_forever()
        server.shutdown()
        server.server_close()


    process = multiprocessing.Process(target=start_server, args=(PAKON_QUERY_SOCK, ready, ))
    process.daemon = True
    process.start()

    ready.wait()
    yield process


    try:
        os.unlink(PAKON_QUERY_SOCK)
    except OSError:
        pass


from foris_controller_testtools.fixtures import backend, infrastructure, ubusd_test


def test_perform_query(mocked_pakon_server, infrastructure, ubusd_test):
    notifications = infrastructure.get_notifications()
    res = infrastructure.process_message({
        "module": "pakon",
        "action": "perform_query",
        "kind": "request",
        "data": {
            "query_data": "{}"
        }
    })
    assert "response_data" in res["data"]
    # try to parse json (response should be json)
    json.loads(res["data"]["response_data"])
