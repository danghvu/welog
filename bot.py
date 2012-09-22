from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log
import database

import time, sys

class MessageLogger:

    def __init__(self):
        self.storage = database.dbClient

    def log(self, message):
        """Save message to storage"""
        pass

    def close(self):
        #self.storage.close()
        pass

class LogBot(irc.IRCClient):

    nickname = "logbot"
    
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.logger = MessageLogger()
        log.msg("[connected at %s]" % time.asctime(time.localtime(time.time())))

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        log.msg("[disconnected at %s]" % time.asctime(time.localtime(time.time())))

    def signedOn(self):
        """Since the Protocol instance is recreated each time the connection is made, the client needs some way to keep track of data that should be persisted. It has reference to the factory that create it"""
        self.join(self.factory.channel)

    def joined(self, channel):
        pass

    def privmsg(self, user, channel, msg):
        """Call when bot receive a message"""
        #TODO: save to database
        log.msg("user %s - channel %s - msg %s" % (user, channel, msg))

        
class LogBotFactory(protocol.ClientFactory):

    def __init__(self, channel):
        self.channel = channel
    
    def buildProtocol(self, addr):
        p = LogBot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        reactor.stop()

def createBot(channel, irc_server, irc_port):
    f = LogBotFactory(channel)
    #TODO: add SSL support
    reactor.connectTCP(irc_server, irc_port, f)
    return f
    