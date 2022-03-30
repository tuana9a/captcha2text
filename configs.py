import os
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

PORT = os.getenv("PORT")
BIND = os.getenv("BIND")
DEVICE = os.getenv("DEVICE")
