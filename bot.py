from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, threads
from twisted.python import log
from database import dbClient 

import time, sys
import re


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

    #TODO: how should nickname change when listening on multiple channel ? at the moment Worker__, Worker___, Worker____ ..
    nickname = "Worker__"

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.logger = MessageLogger()
        log.msg("[connected at %s]" % time.asctime(time.localtime(time.time())))

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        log.msg("[disconnected at %s]" % time.asctime(time.localtime(time.time())))

    def signedOn(self):
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
bot_load = {}

def createBot(channel, irc_server="irc.freenode.net", irc_port=6667):
    #prevent input of unicode channel name
    channel = str(channel)
    #match RFC 1459
    if (re.match("[#&][^\x07\x2C\s]{,200}",channel) is None):
        return False

    # TODO: should we reuse the old connection ? if it's in the same server ? 
    log.msg("Creating bot listening on channel %s" % channel)
    #f = LogBotFactory(channel)
    #reactor.connectTCP(irc_server, irc_port, f)
    #global bots
    #bots[channel] = f

    global abots, bots

    if channel in bots: return False

    reuse = None
    for bot in bot_load.iterkeys():
        if bot_load[bot] < 2: #TODO: move "2" as settings MAX_CHANNEL_PER_BOT
            reuse = bot
            bot_load[bot]+=1

    if (reuse is None):
        f = LogBotFactory(channel)
        reactor.connectTCP(irc_server, irc_port, f)
        reuse = f
        bot_load[reuse] = 1
    else:
        reuse.client.join(channel)
    
    bots[channel] = reuse

    return True
    #TODO: add SSL support

def startLogWorker(channel):
    if channel not in bots:
        return threads.blockingCallFromThread(reactor, createBot, channel)

def stopLogWorker(channel):
    global bots
    if channel in bots:
        bots[channel].disconnect()
        del bots[channel]

def isChannelListened(channel):
    if channel in bots:
        return True
    return False
    
from threading import Thread
import sys

botThread = None
def startBotService(): 
    reactor.callFromThread(log.startLogging, sys.stdout)
    botThread = Thread(target=reactor.run, args=(False,))
    botThread.daemon = True
    botThread.start()

#def stopBot(channel):
def stopBotService():
    botThread.stop() 
    botThread.join()
   
if __name__ == '__main__':
    log.startLogging(sys.stdout)
    f = createBot('#vithon')
    reactor.run()
