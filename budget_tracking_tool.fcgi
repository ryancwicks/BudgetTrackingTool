#!/usr/bin/python
from flup.server.fcgi import WSGIServer
from budget_tracking_tool import create_application

if __name__ == '__main__':
    app = create_application("Production")
    WSGIServer(app).run()