#!/usr/bin/python

# for starting this from hand:
# sudo influxd
# sudo service grafana-server start
# ./bierboerse.py

import time
import BaseHTTPServer
from influxdb import InfluxDBClient
import json
import re


HOST_NAME = '0.0.0.0' 
PORT_NUMBER = 8000

global config


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
        s.wfile.write(
	"<html><head><title>Title goes here.</title>"
        "    <meta charset=\"utf-8\"/>"
        "</head>\n"
	"<body>\n")
	for beername in config["beer"]:
	    s.wfile.write(
	    "    <form action=\"" + clean(beername) + "\" method=\"post\">\n"
	    "        <button name=\"foo\" value=\"upvote\">" + beername + "</button>\n"
	    "    </form>\n")
	s.wfile.write("</body></html>\n")
    def do_POST(s):
        alpi = 0
        print str(s.path) + "PATHAT"
        for beer in config["beer"]:
            if str(s.path) == "/" + clean(beer):
                config["beer"][beer]["amount"] -= 1
                client.write_points(
                    [{
                        "measurement": clean(beer),
                        "fields": {
                            "value": int(config["beer"][beer]["amount"])
                        }
                    }]
                )
                print "Ein " + beer + " wurde gekauft."
        s.send_response(204)

def clean(str):
    str = str.strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', str)

if __name__ == '__main__':
    with open('/home/justin/git/bierboerse/data.json') as data_file:    
    	config = json.load(data_file)
    print config
    client = InfluxDBClient(host='127.0.0.1', database='bierboerse')
    # client.create_database('bierboerse') # database should be created by systemdservice
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

