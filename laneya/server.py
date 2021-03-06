import sys

from twisted.python import log
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from twisted.internet import task

import protocol


class User(object):
    def __init__(self, position_x=0, position_y=0, direction='stop'):
        self.position_x = position_x
        self.position_y = position_y
        self.direction = direction


class ServerProtocol(protocol.ServerProtocol):
    def requestReceived(self, user, action, **kwargs):  # TODO
        if user not in self.factory.users:
            self.factory.users[user] = User()
            print("login %s" % user)

        if action == 'echo':
            return kwargs
        elif action == 'move':
            self.factory.users[user].direction = kwargs['direction']
            return {}
        elif action == 'logout':
            del self.factory.users[user]
            print("logout %s" % user)
            return {}
        else:
            self.broadcastUpdate(action, **kwargs)
            reactor.callLater(5, self.broadcastUpdate, action, **kwargs)
            return {}


class Server(protocol.ServerProtocolFactory):
    def __init__(self):
        protocol.ServerProtocolFactory.__init__(self, ServerProtocol)
        self.users = {}

    def mainloop(self):
        for key, user in self.users.iteritems():
            if user.direction == 'north':
                user.position_y -= 1
            elif user.direction == 'east':
                user.position_x += 1
            elif user.direction == 'south':
                user.position_y += 1
            elif user.direction == 'west':
                user.position_x -= 1
            if user.direction != 'stop':
                self.broadcastUpdate(
                    'position',
                    x=user.position_x,
                    y=user.position_y,
                    entity=key)


def main():
    log.startLogging(sys.stdout)
    server = Server()
    endpoint = TCP4ServerEndpoint(reactor, 5001)
    endpoint.listen(server)

    mainloop = task.LoopingCall(server.mainloop)
    mainloop.start(0.1)

    reactor.run()


if __name__ == '__main__':  # pragma: nocover
    main()
