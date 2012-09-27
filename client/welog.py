import sys
sys.path.append(".")

from flask import Flask, render_template, request, abort
import os,json

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
    
    return render_template("index.html", logs = dblogs, channel_list=channels)

@app.route('/<name>/ajax/')
def channel_ajax(name):
    from database import dbClient

    dblogs = nicePrint( dbClient.read(channel=name) )
    return json.dumps( dblogs )

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
