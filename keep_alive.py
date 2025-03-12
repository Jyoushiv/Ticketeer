from flask import Flask
from threading import Thread
import logging

# Setup flask app
app = Flask(__name__)

# Disable excessive Flask logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def home():
    """
    Simple route to respond to pings to keep the Replit alive.
    """
    return "Ticket Bot is alive!"

def run():
    """
    Run the Flask app on a separate thread.
    """
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    """
    Create and start a thread that runs the Flask app.
    """
    t = Thread(target=run)
    t.daemon = True  # Set as daemon so it closes when the main program exits
    t.start()
    logging.info("Keep-alive server started on port 8080")