#!/usr/bin/python
import time
import datetime
import BaseHTTPServer


HOST_NAME = 'localhost' 
PORT_NUMBER = 8000


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
        print "Ein Bier wurde gekauft."
        print s.path
        print s.headers
        with open("alpi.csv", "a") as myfile:
            myfile.write(str(datetime.datetime.now()) + "\n")
        s.send_response(204)

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

