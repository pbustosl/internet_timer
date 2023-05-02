from http.server import BaseHTTPRequestHandler, HTTPServer
from cgi import parse_header, parse_multipart
from urllib.parse import parse_qs
from datetime import datetime, timedelta
import time

import json

host_name = "0.0.0.0"
host_port = 9001
time_limit = datetime.now() + timedelta(days = -1)

class MyServer(BaseHTTPRequestHandler):
  def __init__(self, *args):
    BaseHTTPRequestHandler.__init__(self, *args)

  def set_time_limit(self, minutes):
    global time_limit
    time_limit = datetime.now() + timedelta(minutes = minutes)

  def write_page(self):
    f = open("index.html", 'rb')
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()
    self.wfile.write(f.read())
    self.wfile.write(bytes(f'<p>time limit:<br>{time_limit.strftime("%m/%d/%Y %H:%M:%S") if time_limit>datetime.now() else "not set"}</p>',"utf-8"))
    f.close()

  def do_GET(self):
    if self.path == '/time_limit':
      self.send_response(200)
      self.send_header("Content-type", "text/html")
      self.end_headers()
      self.wfile.write(bytes(f'{time.mktime(time_limit.timetuple())}',"utf-8"))
    else:
      self.write_page()

  def parse_POST(self):
    ctype, pdict = parse_header(self.headers['content-type'])
    if ctype == 'multipart/form-data':
      postvars = parse_multipart(self.rfile, pdict)
    elif ctype == 'application/x-www-form-urlencoded':
      length = int(self.headers['content-length'])
      postvars = parse_qs(
        self.rfile.read(length),
        keep_blank_values=1)
    else:
      postvars = {}
    return postvars

  def do_POST(self):
    postvars = self.parse_POST()
    print(postvars)
    self.set_time_limit(int(postvars[b'minutes'][0]))
    self.write_page()

myServer = HTTPServer((host_name, host_port), MyServer)

try:
  myServer.serve_forever()
except KeyboardInterrupt:
  pass

myServer.server_close()
