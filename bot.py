from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log
from database import dbClient 

import time, sys


class MessageLogger:

    def __init__(self):
        self.storage = dbClient 

    def log(self, user, channel, message):
        try:
            self.storage.write(user,channel,message)
        except Exception as e:
            raise RuntimeError("Can't write to the storage: " + str(e))

def close(self):
    #self.storage.close()
        pass

class LogBot(irc.IRCClient):

    nickname = "Worker__"

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.logger = MessageLogger()
        log.msg("[connected at %s]" % time.asctime(time.localtime(time.time())))

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        log.msg("[disconnected at %s]" % time.asctime(time.localtime(time.time())))

    def signedOn(self):
        #Since the Protocol instance is recreated each time the connection is made, the client needs some way to keep track of data that should be persisted. It has reference to the factory that create it
        self.join(self.factory.channel)

    def joined(self, channel):
        log.msg("Bot has joined channel %s" % channel)

    def privmsg(self, user, channel, msg):
        """Call when bot receive a message"""
        user = user.split('!', 1)[0]
        log.msg("user %s - channel %s - msg %s" % (user, channel, msg))

        self.logger.log( user, channel, msg )

        if channel == self.nickname:
            #TODO: when user initiate private conversation with bot
            log.msg("User %s on private channel" % user) 

class LogBotFactory(protocol.ClientFactory):

    def __init__(self, channel):
        self.channel = channel
    
    def buildProtocol(self, addr):
        p = LogBot()
        p.factory = self
        self.client = p
        return p

    def disconnect(self):
        self.client.quit()

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        log.msg("[Connection Failed: %s" % reason)
        reactor.stop()

bots = {}

def createBot(channel, irc_server="irc.freenode.net", irc_port=6667):
    #prevent input of unicode channel name
    channel = str(channel)

    log.msg("Creating bot listening on channel %s" % channel)
    f = LogBotFactory(channel)
    reactor.connectTCP(irc_server, irc_port, f)
    global bots
    bots[channel] = f
    #TODO: add SSL support

def startLogWorker(channel):
    print 'Create bot for channel %s ' % channel
    #bot = createBot(channel) 
    if channel not in bots:
        reactor.callFromThread(createBot, channel)

def stopLogWorker(channel):
    global bots
    if channel in bots:
        bots[channel].disconnect()
        del bots[channel]
    
from threading import Thread
import sys

botThread = None
def startBotService(): 
    botThread = Thread(target=reactor.run, args=(False,))
    botThread.start()
    reactor.callFromThread(log.startLogging, sys.stdout)
#def stopBot(channel):

def stopBotService():
    botThread.stop() 

if __name__ == '__main__':
    log.startLogging(sys.stdout)
    f = createBot('#vithon')
    reactor.run()
    
