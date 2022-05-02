# THIS LENTO CLI IS FOR DEVELOPER USE ONLY. DO NOT
# ATTEMPT TO USE THIS FOR SCRIPTING PURPOSES. END-USER
# USE OF THIS SCRIPT IS NOT SUPPORTED. WE USE THIS
# SCRIPT FOR LIVE-AMMO TESTING OF THE BACKEND; USING
# IT WITH LENTO MAY HAVE UNINTENDED OR UNEXPECTED
# CONSEQUENCES.
import argparse
import copy
import json
import os
import platform
from lento.common import cards_management as CardsManagement
from lento import utils
from lento.common import get_block_controller
from tests import helpers

parser = argparse.ArgumentParser(
    description="Run backend functions to make sure they work."
)
parser.add_argument(
    "name",
    type=str,
    help="name of function to run"
)
parser.add_argument("param1", nargs='?')
parser.add_argument("param2", nargs='?')
parser.add_argument("param3", nargs='?')
parser.add_argument("param4", nargs='?')
parser.add_argument("param5", nargs='?')
parser.add_argument("param6", nargs='?')
parser.add_argument("param7", nargs='?')
parser.add_argument("param8", nargs='?')
parser.add_argument("param9", nargs='?')
parser.add_argument("param10", nargs='?')

args = parser.parse_args()
f = args.name
param1 = args.param1
param2 = args.param2
param3 = args.param3
param4 = args.param4
param5 = args.param5
param6 = args.param6
param7 = args.param7
param8 = args.param8
param9 = args.param9
param10 = args.param10

result_options = {
    "message": f"ran {f} successfully!",
    "output": None,
}

if f == "create_card":
    CardsManagement.create_card(param1)
    result_options["output"] = CardsManagement.read_cards()
elif f == "read_cards":
    result_options["output"] = CardsManagement.read_cards()
elif f == "delete_card":
    CardsManagement.delete_card(param1)
    result_options["output"] = CardsManagement.read_cards()
elif f == "update_metadata":
    CardsManagement.update_metadata(param1, param2, param3)
    result_options["output"] = CardsManagement.read_cards()
elif f == "add_to_site_blocklists":
    CardsManagement.add_to_site_blocklists(param1, param2, param3)
    result_options["output"] = CardsManagement.read_cards()
elif f == "update_site_blocklists":
    CardsManagement.update_site_blocklists(
        param1,
        param2,
        {
            "youtube.com": True,
            "twitter.com": False
        }
    )
    result_options["output"] = CardsManagement.read_cards()
elif f == "add_to_app_blocklists":
    if platform.system() == "Windows":
        apps_to_add = copy.deepcopy(helpers.data["apps_to_add"])
        apps_to_add[1]["path"] = os.path.join(
            os.path.expanduser("~"),
            "AppData",
            "Local",
            "Vivaldi",
            "Application",
            "vivaldi.exe"
        )
        apps_to_add[1]["icon_path"] = os.path.join(
            os.path.expanduser("~"),
            "AppData",
            "Local",
            "Lento",
            "vivaldi.bmp"
        )
        CardsManagement.add_to_app_blocklists(
            param1,
            param2,
            apps_to_add
        )
        result_options["output"] = CardsManagement.read_cards()
    elif platform.system() == "Darwin":
        CardsManagement.add_to_app_blocklists(
            param1,
            param2,
            [
                "/Applications/GRIS.app",
                "/Applications/Scrivener.app",
                "/Applications/NetNewsWire.app"
            ]
        )
        result_options["output"] = CardsManagement.read_cards()
elif f == "get_apps":
    r = utils.get_apps()
    result_options["output"] = r
elif f == "update_app_blocklists":
    if platform.system() == "Windows":
        CardsManagement.update_app_blocklists(
            param1,
            param2,
            {
                "vivaldi": {
                    "enabled": True,
                    "path": "C:\\Users\\natha\\AppData\\Local\\Vivaldi\\Application\\vivaldi.exe",  # noqa: E501
                    "app_icon_path": "C:\\Users\\natha\\AppData\\Local\\Lento\\vivaldi.bmp"  # noqa: E501
                },
                "Trello": {
                    "enabled": False,
                    "path": "C:\\Program Files\\WindowsApps\\45273LiamForsyth.PawsforTrello_2.12.5.0_x64__7pb5ddty8z1pa\\app\\Trello.exe",  # noqa: E501
                    "app_icon_path": "C:\\Program Files\\WindowsApps\\45273LiamForsyth.PawsforTrello_2.12.5.0_x64__7pb5ddty8z1pa\\assets\\Square310x310Logo.scale-200.png"  # noqa: E501
                }
            }
        )
    elif platform.system() == "Darwin":
        CardsManagement.update_app_blocklists(
            param1,
            param2,
            {
                "Scrivener": {
                    "enabled": True,
                    "bundle_id": "com.literatureandlatte.scrivener3",
                    "app_icon_path": "~/Library/Application Support/Lento/Scrivener.jpg"  # noqa: E501
                },
                "NetNewsWire": {
                    "enabled": True,
                    "bundle_id": "com.ranchero.NetNewsWire-Evergreen",
                    "app_icon_path": "~/Library/Application Support/Lento/NetNewsWire.jpg"  # noqa: E501
                },
                "GRIS": {
                    "enabled": True,
                    "bundle_id": "unity.nomada studio.GRIS",
                    "app_icon_path": "~/Library/Application Support/Lento/GRIS.jpg"  # noqa: E501
                },
            }
        )
elif f == "add_notification":
    CardsManagement.add_notification(
        param1,
        True,
        param2,
        "banner",
        ["twitter.com", "youtube.com"],
        ["Debug USACO problem"],
        42,
        "get back to work",
        "keep focused",
        {
            "reminder": "~/Desktop/reminder.mp3",
            "Frog": "/System/Library/Sounds/Frog.aiff"
        }
    )
elif f == "update_notification_list":
    CardsManagement.update_notification_list(
        param1,
        {
            "2d189b37-6eaf-478f-a5ab-e19c9dab5738": {
                "name": "testnotif2",
                "enabled": True,
                "type": "banner",
                "blocked_visit_triggers": [
                    "twitter.com",
                    "youtube.com"
                ],
                "associated_goals": [
                    "Debug USACO problem"
                ],
                "time_interval_trigger": 42,
                "title": "get back to work",
                "body": "keep focused",
                "audio_paths": {
                    "reminder": "~/Desktop/reminder.mp3",
                    "Frog": "/System/Library/Sounds/Frog.aiff"
                }
            },
            "ba606651f167406ca7cd88a8c9b05ceb": {
                "name": "testnotif1",
                "enabled": True,
                "type": "banner",
                "blocked_visit_triggers": [
                    "twitter.com",
                    "youtube.com"
                ],
                "associated_goals": [
                    "Debug USACO problem"
                ],
                "time_interval_trigger": 42,
                "title": "get back to work",
                "body": "keep focused",
                "audio_paths": {
                    "reminder": "~/Desktop/reminder.mp3",
                    "Frog": "/System/Library/Sounds/Frog.aiff"
                }
            }
        },
    )
elif f == "add_goal":
    CardsManagement.add_goal(param1, param2)
elif f == "update_goal_list":
    CardsManagement.update_goal_list(param1, {
        "Conquer world": True,
        "Debug USACO problem": False,
    })
elif f == "daemon":
    result_options["message"] = "WARNING: run `python3 -m lento.daemon` for live-ammo testing of daemon and/or proxy"  # noqa: E501
elif f == "start_block":
    block_controller = get_block_controller()
    block_controller.start_block(param1, param2)
elif f == "end_block":
    block_controller = get_block_controller()
    block_controller.end_block()
elif f == "get_remaining_block_time":
    block_controller = get_block_controller()
    result_options["output"] = block_controller.get_remaining_block_time()
else:
    result_options["message"] = f"INVALID COMMAND: {f}"

print(result_options["message"])
if result_options["output"] is not None:
    print("OUTPUT:")
    print(json.dumps(result_options["output"], indent=4))
