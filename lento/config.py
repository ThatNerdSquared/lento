"""App instance configuration."""
import os
import dotenv
from pathlib import Path
from lento import utils

dotenv.load_dotenv(dotenv_path=utils.get_data_file_path('.env'), override=True)


class Config:
    TEST_VAR = os.getenv('TEST_VAR')
    MACOS_APPLICATION_FOLDER = Path("/Applications/")
