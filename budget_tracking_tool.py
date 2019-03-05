"""
Main entry point for the budget tracking tool.
"""
import os
from budget_tracking_tool import create_application
import webbrowser
import threading

app = create_application (os.getenv('BUDGET_TRACKER_APP_CONFIG') or 'default')

def main():
    port = 5000 #+ random.randint(0, 999)
    url = 'http:/127.0.0.1:' + str(port)
    if not app.config['DEBUG']:
        threading.Timer (1.25, lambda: webbrowser.open_new(url) ).start()
    app.run(host="0.0.0.0", port=port)

if __name__ == '__main__':
    main()
