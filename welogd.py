#!/usr/bin/env python
#from twisted.web import server, resource
from twisted.internet import reactor
from twisted.python import log
from bot import createBot 
from threading import Thread
import sys

#class LogServer(resource.Resource):
    #isLeaf = True
    #irc_servers = {} 

    #def render_POST(self, request):
        #channel = request.args.get("c")[0] 
        #server = request.args.get("s")[0]
        #port = request.args.get("p")
        #if not port:
            #port = 6667
        #else:
            #port = int(port[0])
        ##check if same channel server bot already exist
        #log.msg("Request for Listening on server: %s:%s - channel: %s" % (server, port, channel))
        #if channel in self.irc_servers.get(server, {}):
            #log.msg('Channel is already listened')
            #return "{status: 404}"

        #logBot = bot.createBot(channel, server, port)
        #self.irc_servers.setdefault(server, {})[channel] = logBot
        #return "{status: 200}"

    #def render_DELETE(self, request):
        #"""DELETE request to stop LogBot"""
        #channel = request.args.get("c")[0] 
        #server = request.args.get("s")[0]
        ##get LogBot
        #if not self.irc_servers.get(server, None) or not self.irc_servers.get(server).get(channel, None):
            #log.msg("No bot listening on server %s - channel %s" % (server, channel))
            #return "{status: 404}"
        #logBot = self.irc_servers.get(server).get(channel)
        #logBot.disconnect()
        #return "{status:200}"


#def startLogging(channel):
    #print 'Create bot for channel %s ' % channel
    ##bot = createBot(channel) 
    #reactor.callFromThread(createBot, channel)

#def stopLogging(channel):
    #bots[channel].disconnect()
    
#def startService(): 
    #Thread(target=reactor.run, args=(False,)).start()
    #reactor.callFromThread(log.startLogging, sys.stdout)

#if __name__ == "__main__":
    #log.startLogging(sys.stdout)
    #site = server.Site(LogServer())

    #if len(sys.argv) < 2: port = 8080
    #else: port = int(sys.argv[1])

    #reactor.listenTCP(port, site)

    #reactor.run()bkitsec

