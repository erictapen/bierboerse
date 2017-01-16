#!/usr/bin/python

# sudo influxd
# sudo service grafana-server start
# ./bierboerse.py

import time
import BaseHTTPServer
from influxdb import InfluxDBClient


HOST_NAME = '0.0.0.0' 
PORT_NUMBER = 8000

global alpi
global pils


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>Title goes here.</title></head>")
        s.wfile.write("<body>")
        s.wfile.write("    <form action=\"pils\" method=\"post\">")
        s.wfile.write("        <button name=\"foo\" value=\"upvote\">Pils</button>")
        s.wfile.write("    </form>")
        s.wfile.write("    <form action=\"alpi\" method=\"post\">")
        s.wfile.write("        <button name=\"foo\" value=\"upvote\">Alpi</button>")
        s.wfile.write("    </form>")
        s.wfile.write("</body></html>")
    def do_POST(s):
        global alpi
        global pils
        print str(s.path) + "PATHAT"
        if str(s.path) == "/alpi":
            client.write_points(
                [{
                    "measurement": "alpi",
                    "fields": {
                        "value": alpi
                    }
                }]
            )
            alpi += 1
            print "Ein Alpi wurde gekauft."
        if str(s.path) == "/pils":
            client.write_points(
                [{
                    "measurement": "pils",
                    "fields": {
                        "value": pils
                    }
                }]
            )
            pils += 1
            print "Ein Pils wurde gekauft."
        s.send_response(204)

if __name__ == '__main__':
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'bierboerse')
    client.create_database('bierboerse')
    alpi = 0
    pils = 0
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

