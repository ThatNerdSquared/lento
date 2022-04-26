import json
from lento.config import Config


def init_sequence():
    init_needed = False

    # Check for the lentosettings.json file, create if nonexistent
    try:
        Config.SETTINGS_PATH.read_text()
    except FileNotFoundError:
        blank_config = {
            "activated_card": None,
            "cards": {},
            "application_settings": {
                "theme": "automatic"
            }
        }
        Config.SETTINGS_PATH.write_text(json.dumps(blank_config))
        init_needed = True

    # Create the correct application data folder for the platform, unless it
    # exists already.
    try:
        Config.APPDATA_PATH.mkdir(parents=True)
        init_needed = True
    except FileExistsError:
        pass

    return init_needed
