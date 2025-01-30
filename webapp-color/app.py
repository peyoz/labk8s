import os
import random
import argparse
from datetime import datetime
import logging
import socket
from flask import Flask, render_template


app = Flask(__name__)

# Define color codes and supported colors
color_codes = {
    "red": "#e74c3c",
    "green": "#16a085",
    "blue": "#2980b9",
    "blue2": "#30336b",
    "pink": "#be2edd",
    "darkblue": "#130f40"
}

SUPPORTED_COLORS = ",".join(color_codes.keys())

# Setup logging
logging.basicConfig(level=logging.INFO)

def get_color_from_args():
    """Parse command line arguments to get the color."""
    parser = argparse.ArgumentParser(description="A sample web application that displays a colored background.")
    parser.add_argument('--color', choices=color_codes.keys(), help=f"Color to display. Must be one of {SUPPORTED_COLORS}.")
    args = parser.parse_args()
    return args.color

def determine_color():
    """Determine the color based on command line argument, environment variable, or random choice."""
    color_from_arg = get_color_from_args()
    if color_from_arg:
        logging.info(f"Color from command line argument: {color_from_arg}")
        return color_from_arg
    elif COLOR_FROM_ENV := os.environ.get('APP_COLOR'):
        logging.info(f"Color from environment variable: {COLOR_FROM_ENV}")
        return COLOR_FROM_ENV
    else:
        color = random.choice(list(color_codes.keys()))
        logging.info(f"No command line argument or environment variable. Picking a Random Color: {color}")
        return color

@app.route("/")
def main_route():
    """Render the main page with the determined color and contents."""
    global name, contents
    COLOR_FROM_ENV = os.environ.get('APP_COLOR')
    COLOR = determine_color()

    if COLOR not in color_codes:
        logging.error(f"Color not supported. Received '{COLOR}', expected one of {SUPPORTED_COLORS}")
        exit(1)

    STATIC = os.environ.get("STATIC", "false").lower() == "true"

    if STATIC:
        data_file_path = "/data/data-id.txt"
        os.makedirs(os.path.dirname(data_file_path), exist_ok=True)
        timestamp_line = f"Startup executed: {datetime.now().isoformat()}\n"
        with open(data_file_path, "a") as file:
            file.write(timestamp_line)
        with open(data_file_path, "r") as file:
            contents = file.read()
    else:
        logging.info("Dynamic mode: 'name' variable initialized with the hostname.")

    return render_template('hello.html', name=name, color=color_codes[COLOR], contents=contents)

if __name__ == "__main__":
    # Initialize global variables
    name = socket.gethostname()
    contents = ""

    # Print description of how the application works
    print("This is a sample web application that displays a colored background.")
    print("A color can be specified in two ways:")
    print("\n1. As a command line argument with --color as the argument. Accepts one of " + SUPPORTED_COLORS)
    print("2. As an Environment variable APP_COLOR. Accepts one of " + SUPPORTED_COLORS)
    print("3. If none of the above then a random color is picked from the above list.")
    print("Note: Command line argument takes precedence over the environment variable.\n")

    # Start the Flask application
    app.run(host="0.0.0.0", port=8080)