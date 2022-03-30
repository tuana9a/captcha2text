import os
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

PORT = os.getenv("PORT") or 80
BIND = os.getenv("BIND") or "0.0.0.0"
DEVICE = os.getenv("DEVICE") or "cpu"
