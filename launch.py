# Launch backend.api on port 5000 (backend)
# Launch http.server on port 3000 (frontend)
import http.server
import socketserver
from threading import Thread
import uvicorn

# run backend.api on port 5000 (backend) in a separate subprocess
backendThread = Thread(target=uvicorn.run, args=('API.API:app',), kwargs={'port': 5000})
backendThread.start()

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="frontend", **kwargs)


with socketserver.TCPServer(("", 80), Handler) as httpd:
    httpd.serve_forever()

backendThread.join()