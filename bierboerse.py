#!/usr/bin/python

# for starting this from hand:
# sudo influxd
# sudo service grafana-server start
# ./bierboerse.py

import time
import BaseHTTPServer
from influxdb import InfluxDBClient
import sys
import json
import base64


HOST_NAME = '0.0.0.0' 
PORT_NUMBER = 8000

global config
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
        s.wfile.write(
	"<html><head><title>Title goes here.</title></head>\n"
	"<body>\n"
        "    <form action=\"alpi\" method=\"post\">\n"
	"        <button name=\"foo\" value=\"upvote\">Alpi</button>\n"
	"    </form>\n")
	for beerstring in config["beer"]:
	    s.wfile.write(
	    "    <form action=\"" + clean(beerstring) + "\" method=\"post\">\n"
	    "        <button name=\"foo\" value=\"upvote\">Alpi</button>\n"
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
                        "measurement": "bla", #clean(beer),
                        "fields": {
                            "value": 3.0 #int(config["beer"][beer]["amount"])
                        }
                    }]
                )
                print "Ein " + beer + " wurde gekauft."
                
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

def clean(str):
    return base64.urlsafe_b64encode(str)

if __name__ == '__main__':
    with open('data.json') as data_file:    
    	config = json.load(data_file)
    print config
#    for beer in config["beer"]:
#        config["beer"]["id"] = base64.urlsafe_b64encode(beer)
    client = InfluxDBClient(host='127.0.0.1', database='bierboerse')
    # client.create_database('bierboerse') # database should be created by systemdservice
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

