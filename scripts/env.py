from dotenv import load_dotenv
from pathlib import Path
import os


def env_path(name):
    return Path(os.environ[name])

load_dotenv()