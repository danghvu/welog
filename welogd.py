#!/usr/bin/env python
from twisted.web import server, resource
from twisted.words.protocols import irc
from twisted.internet import reactor
import bot

class LogServer(resource.Resource):
    isLeaf = True
    server_list = {} 

    def render_POST(self, request):
        channel = request.args.get("c") 
        server = request.args.get("s")
        #check if same channel server bot already exist
        if channel in self.server_list.get(server, {}):
            print 'Channel is already listened'
            return "{status: 404}"

        logBot = bot.createBot(channel, server, 6667)
        self.server_list.set_default(server, {})[channel] = logBot
        return "{status: 200}"

    def render_GET(self, request):
        """Testing"""
        channel = "abc"
        server = "irc.freenode.net"
        logBot = bot.createBot(channel, server, 6667)
        return "OK"

    def render_DELETE(self, request):
        pass

if __name__ == "__main__":
    site = server.Site(LogServer())
    reactor.listenTCP(8080, site)
    reactor.run()

