import io
import os
import sys
import dotenv
import yaml
import werkzeug

from PIL import Image
from flask import Flask, request, render_template
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg

dotenv.load_dotenv(dotenv.find_dotenv())

PORT = os.getenv("PORT") or 8080
BIND = os.getenv("BIND") or "0.0.0.0"
DEVICE = os.getenv("DEVICE") or "cpu"
SECRET = os.getenv("SECRET")
ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5mb

predictor_config = Cfg({})


def is_allowed_extension(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


with open("./weights/config.yaml") as f:
    predictor_config = Cfg(yaml.safe_load(f))
    predictor_config["device"] = DEVICE
    predictor = Predictor(predictor_config)

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(MAX_CONTENT_LENGTH=MAX_UPLOAD_SIZE)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def upload_image():
    # check file exist
    if "file" not in request.files:
        return "file is not exist in request"
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
    except Exception as err:
        app.logger.error(f"{upload_image.__name__}(): {err}")
        return "error"


@app.route("/change_device", methods=["GET"])
def change_device():
    global predictor
    device = request.args.get("device", "cpu")
    secret = request.headers.get("secret")
    try:
        if secret != SECRET:
            return "secret is not correct"
        predictor_config["device"] = device
        predictor = Predictor(predictor_config)
        return device
    except Exception as err:
        app.logger.error(f"{change_device.__name__}(): {err}")
        return "error"


def main():
    app.logger.info(f" * Listen http://{BIND}:{PORT}")
    app.run(host=BIND, port=PORT, debug=False)


if __name__ == "__main__":
    try:
        main()
    except:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
