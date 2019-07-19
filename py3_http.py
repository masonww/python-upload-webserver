import sys
import http.server
import socketserver
import cgi
import os
import _thread as thread
import urllib.parse as urlparse

####
#### An HTTPRequestHandler designed to receive files in multiple ways
####
#### v1.0.1
#### by WindsorKingdom
####

class FileReceiving_HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        print("[I got a POST request]")
        print("=====Headers=====")
        print(self.headers)
        
        print("=====Path=====")
        print(self.path)
        
        if(self.path.startswith('/shutdown')):
            print("Server is shutting down")
            def killServer(serv):
                serv.shutdown()
            thread.start_new_thread(killServer, (server,))
            self.send_error(500)
            return
        
        data = self.rfile.read(int(self.headers['Content-Length']))
        print('=====Saving to the file=====')
        #  get the resulting filename from "server:port/path", fails if no path is given
        #  turn '/' into './' to make it relative instead of absolute
        savePath = os.path.normpath(os.path.join(os.getcwd(), "." + self.path))
        print(savePath)
        
        #  overwrite existing
        with open(savePath, 'w') as filehandler:
            filehandler.write(data.decode())
        
        self.send_response(http.HTTPStatus.ACCEPTED)
        self.end_headers()
        print('[End of request handling]')
    def do_GET(self):
        print("[I got a GET request]")
        print("=====Headers=====")
        print(self.headers)
        print("=====Path=====")
        print(self.path)
        parsed = urlparse.urlparse(self.path)
        print(parsed)
        print("Query: " + parsed.query)
        print("")
        
        if(parsed.query != ""):
            print('=====Saving query to the file=====')
            savePath = os.path.normpath(os.path.join(os.getcwd(), "query.txt"))
            print(savePath)
            
            #  overwrite existing
            with open(savePath, 'w') as filehandler:
                filehandler.write(parsed.query)
            
            self.send_response(http.HTTPStatus.ACCEPTED)
            self.end_headers()
        print('[End of request handling]')
port = 80
if len(sys.argv) > 1:
    port = int(sys.argv[1])

with socketserver.TCPServer(("", port), FileReceiving_HTTPRequestHandler, False) as server:
    print("Starting server on port", port)
    print("Current directory: ")
    print(os.getcwd())
    server.allow_reuse_address = True
    server.server_bind()
    server.server_activate()
    print("Server bound and activated")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    print("Server closed")