import http.server
import socketserver
import os
import posixpath
import urllib.parse

PORT = 3000
DIRECTORY = "/root/projects/erikk"

class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def translate_path(self, path):
        path = urllib.parse.unquote(path)
        parts = path.split('?', 1)
        path = parts[0]
        parts = path.split('#', 1)
        path = parts[0]
        
        clean_path = posixpath.normpath(path)
        words = clean_path.split('/')
        words = filter(None, words)
        
        translated = DIRECTORY
        for word in words:
            if os.path.dirname(word):
                continue
            translated = os.path.join(translated, word)
            
        if not os.path.exists(translated) and not translated.endswith('/') and os.path.exists(translated + '.html'):
            translated += '.html'
            
        return translated

socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", PORT), CleanURLHandler) as httpd:
    print("Serving with Clean URLs at port", PORT)
    httpd.serve_forever()
