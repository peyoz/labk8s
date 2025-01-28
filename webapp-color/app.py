from flask import Flask, render_template
import socket
import random
import os
import argparse
from datetime import datetime

app = Flask(__name__)

color_codes = {
    "red": "#e74c3c",
    "green": "#16a085",
    "blue": "#2980b9",
    "blue2": "#30336b",
    "pink": "#be2edd",
    "darkblue": "#130f40"
}

SUPPORTED_COLORS = ",".join(color_codes.keys())

COLOR_FROM_ENV = os.environ.get('APP_COLOR')
COLOR = random.choice(["red", "green", "blue", "blue2", "darkblue", "pink"])

DATA_FILE_PATH = "/data/data-id.txt"
STATIC = os.environ.get("STATIC", "false").lower() == "true"

name = socket.gethostname()
contents = ""

if STATIC:
    os.makedirs(os.path.dirname(DATA_FILE_PATH), exist_ok=True)
    timestamp_line = f"Startup executed: {datetime.now().isoformat()}\n"
    with open(DATA_FILE_PATH, "a") as file:
        file.write(timestamp_line)
    with open(DATA_FILE_PATH, "r") as file:
        contents = file.read()
else:
    print(f"Dynamic mode: 'name' variable initialized with the hostname.")

@app.route("/")
def main():
    return render_template('hello.html', name=name, color=color_codes[COLOR], contents=contents)

if __name__ == "__main__":

    print(" This is a sample web application that displays a colored background. \n"
          " A color can be specified in two ways. \n"
          "\n"
          " 1. As a command line argument with --color as the argument. Accepts one of " + SUPPORTED_COLORS + " \n"
          " 2. As an Environment variable APP_COLOR. Accepts one of " + SUPPORTED_COLORS + " \n"
          " 3. If none of the above then a random color is picked from the above list. \n"
          " Note: Command line argument takes precedence over the environment variable.\n"
          "\n"
          "")

    parser = argparse.ArgumentParser()
    parser.add_argument('--color', required=False)
    args = parser.parse_args()

    if args.color:
        print("Color from command line argument =" + args.color)
        COLOR = args.color
        if COLOR_FROM_ENV:
            print("A color was set through the environment variable -" + COLOR_FROM_ENV + ". However, the color from the command line argument takes precedence.")
    elif COLOR_FROM_ENV:
        print("No Command line argument. Color from environment variable =" + COLOR_FROM_ENV)
        COLOR = COLOR_FROM_ENV
    else:
        print("No command line argument or environment variable. Picking a Random Color =" + COLOR)

    if COLOR not in color_codes:
        print("Color not supported. Received '" + COLOR + "' expected one of " + SUPPORTED_COLORS)
        exit(1)

    app.run(host="0.0.0.0", port=8080)
