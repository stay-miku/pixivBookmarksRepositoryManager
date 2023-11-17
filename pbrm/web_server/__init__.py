import os

from bottle import route, get, run, Bottle
from .. import config
import webbrowser
from .image import get_image, get_ugoira


app = Bottle()


def run_web(host="localhost", port=8080, debug=False):

    script_path = os.path.dirname(__file__).replace("\\", "/")
    app.tem

    app.get("/static/image/<pid>/<page>")(get_image)
    app.get("/static/ugoira/<pid>")(get_ugoira)

    app.run(host=host, port=port, debug=debug)
    # webbrowser.open(f"http://{host}:{port}")
