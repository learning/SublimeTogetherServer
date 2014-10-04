import sys

# detect python's version
python_version = sys.version_info[0]

# Sublime 3 (Python 3.x)
if python_version == 3:
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from socketserver import ThreadingMixIn, TCPServer
    from urllib import parse as urllib

# Sublime 2 (Python 2.x)
else:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
    from SocketServer import ThreadingMixIn, TCPServer
    import urllib

class WebConfigPanel(BaseHTTPRequestHandler):

    def version_string(self):
        '''overwrite HTTP server's version string'''
        return ''