"""HTTPServer for the dwarfs with hats problem

    Runs a HTTPServer with a ThreadingMixIn socket connection.
    Provides a simple API with Routes / and /history
"""
import json
import datetime
import socketserver
import os
import sys
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

import hats

history = {}

SERVER_PORT = 12345

class ServerHandler(BaseHTTPRequestHandler):
    """Handler for the dwarf hats HTTPServer.

    Routes:
        / standart dwarf hats request (GET param X is possible default 10)
        /history returns your history (based on ip).
    """
    def send_success_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
    def do_GET(self):
        ip_addr = self.client_address[0]
        try:
            if history[ip_addr]:
                pass
        except KeyError:
            history[ip_addr] = []
        # get path without GET params
        path_handler = self.path.split('?')[0]
        # GET params
        if len(self.path.split('?')) > 1:
            parameter = {}
            for urlpart in self.path.split('?')[1].split("&"):
                parameter_splitet = urlpart.split("=")
                if len(parameter_splitet) == 2:
                    name_of_parameter = parameter_splitet[0]
                    # min 1 non whitespace character
                    if name_of_parameter.strip():
                        parameter[name_of_parameter.strip()] = parameter_splitet[1]
            print(f'PARAMETER:{parameter}')

        if path_handler == "/" or path_handler == "/history":
            self.send_success_headers()
        if path_handler == "/":
            try:
                x = int(parameter["X"])
            except:
                x = 10
            self.send_hats(x)
        elif path_handler == "/history":
            self.send_history()
        else:
            # send 404 Header if path is invalid
            self.send_response(404)
            self.end_headers()
            return

    def send_hats(self, x=10):
        dwarf_hats = hats.solution(x)
        ip_addr = self.client_address[0]
        response_obj = {"client_ip_address": ip_addr, "X": x, "dwarf_hat": dwarf_hats}
        history[ip_addr].append(response_obj)
        #write logfile
        output_file = open(f"logs_history/{ip_addr}_{datetime.datetime.now()}", "w")
        output_file.write(json.dumps(response_obj))
        output_file.close()
        # send json
        self.wfile.write(json.dumps(response_obj).encode('utf8'))
        return
    def send_history(self):
        ip_addr = self.client_address[0]
        response_obj = {"client_ip_address": ip_addr,
                        "response_count": len(history[ip_addr]),
                        "responses": history[ip_addr]}
        self.wfile.write(json.dumps(response_obj).encode('utf8'))

# found on StackOverflow
class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    """ ThreadedHTTPServer, allows multiple connection """

# init logfile directory

if not os.path.isdir("./logs_history/"):
    try:
        os.mkdir("./logs_history")
    except Exception as e:
        print(e)
        sys.exit(1)

# accept from all conections

try:
    dwarf_server = ThreadedHTTPServer(('0.0.0.0', SERVER_PORT), ServerHandler)
    print(f"Server succesfully Listening on Port: {SERVER_PORT}")
    dwarf_server.serve_forever()
except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    dwarf_server.socket.close()
# maybe address already in use
except Exception as e:
    print(e)
