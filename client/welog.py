import sys
sys.path.append(".")
from flask import Flask, render_template, request, abort
import os,json
from database import dbClient
from twisted.python import log

app = Flask(__name__)

html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
        }


def html_escape(text):
    return "".join(html_escape_table.get(c,c) for c in text)

def nicePrint(log_content):
    dblogs = []
    for line in log_content:
        time = line[0]
        channel = line[1]
        dblogs += ["[%s] [%s]: %s" % (time, channel, ''.join(line[2:])) ]
    return dblogs

@app.route('/')
@app.route('/<name>/')
def index(name=None):

    from database import dbClient

    dblogs = nicePrint( dbClient.read(channel=name) )

    channels = [x[0] for x in dbClient.listChannel()]

    #from welogd import bots
    active_channels = []
    
    return render_template("index.html", logs = dblogs, channel_list=channels, active_list=active_channels)

@app.route('/<name>/ajax/')
def channel_ajax(name):
    from database import dbClient

    dblogs = nicePrint( dbClient.read(channel=name) )
    return json.dumps( dblogs )
    
@app.route('/<name>/ajax/', methods=["POST"])
def channel_ajax_create(name):
    print 'ABC XYZ'
    from bot import startLogWorker
    app.logger.info("Call for start logging")
    startLogWorker(name) 
    return "{message: 'created'}"
    
@app.route('/<name>/ajax/', methods=["DELETE"])
def channel_ajax_delete(name):
    from bot import stopLogWorker

    stopLogWorker(name)
    return "{message: 'done'}"

if __name__ == '__main__':
    from bot import startBotService, stopBotService
    try: 
        startBotService()
        app.run(debug=True,host="0.0.0.0")
    except (KeyboardInterrupt, SystemExit):
        #stop stop bot service
        stopBotService()
        sys.exit()
