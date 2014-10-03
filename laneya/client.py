import sys

from twisted.python import log
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet import reactor

import protocol


def _print(s):
    print(s)


class ClientProtocol(protocol.Protocol):
    def updateReceived(self, command, **kwargs):  # TODO
        print(command, kwargs)


def connected(protocol):  # TODO
    protocol.sendRequest('echo', foo='bar')\
        .then(_print)

    protocol.sendRequest('other', foo='bar')\
        .then(_print)


def main():
    log.startLogging(sys.stdout)
    endpoint = TCP4ClientEndpoint(reactor, 'localhost', 5001)
    endpoint.connect(Factory.forProtocol(ClientProtocol))\
        .addCallback(connected)
    reactor.run()


if __name__ == '__main__':
    main()
