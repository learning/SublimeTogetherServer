import sys

# version of web config panel
__VERSION__ = '0.0.1'

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
        return 'WebConfigPanel/%s Sublime/%s' % (__VERSION__, sublime.version())

    def do_GET(self):
        '''Serve a GET request.'''
        f = self.send_head()
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()

    def do_HEAD(self):
        '''Serve a HEAD request.'''
        f = self.send_head()
        if f:
            f.close()

    def send_head(self):
        '''Send header to the client'''
        pass