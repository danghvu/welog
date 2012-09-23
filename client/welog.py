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
 
@app.route('/')
def index(name=None):
    return render_template("index.html", logs = ["TODO"], channel_list=["dummy1","dummy2","dummy3"])

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
