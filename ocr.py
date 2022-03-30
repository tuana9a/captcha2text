import configs

from vietocr.tool.config import Cfg
from vietocr.tool.predictor import Predictor

config = Cfg.load_config_from_file("weights.yaml")
config["device"] = configs.DEVICE or "cuda:0"
predictor = Predictor(config)
