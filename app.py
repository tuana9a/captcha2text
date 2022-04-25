import io
import os
import sys
import logging
import datetime
import werkzeug
import configs

from PIL import Image
from flask import Flask, request, render_template
from vietocr.tool.config import Cfg
from vietocr.tool.predictor import Predictor

predictor_config = Cfg.load_config_from_file("weights.yaml")
predictor_config["device"] = configs.DEVICE
predictor = Predictor(predictor_config)

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(MAX_CONTENT_LENGTH=5 * 1024 * 1024)
werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.setLevel(logging.ERROR)
allowed_extensions = ["png", "jpg", "jpeg"]


def is_allowed_extension(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def upload():
    # check file exist
    if "file" not in request.files:
        return "file not exist in request"
    # get the file
    file = request.files["file"]
    if not file:
        return "file is empty"
    # get file name
    filename = werkzeug.utils.secure_filename(file.filename)
    if not is_allowed_extension(filename):
        return filename + " is not allowed"
    # start process
    try:
        buffers = file.stream._file.getvalue()
        image = Image.open(io.BytesIO(buffers))
        result = predictor.predict(img=image)
        return result
    except:
        pattern = "%Y-%m-%d %H:%M:%S" + " error when handle image"
        now = datetime.datetime.now().strftime(pattern)
        print(str(now))
        return "error"


def main():
    bind = configs.BIND
    port = configs.PORT
    print(f' * Listen http://{bind}:{port}')
    app.run(host=bind, port=port, debug=False)


if __name__ == "__main__":
    try:
        main()
    except:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
