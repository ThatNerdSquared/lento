# THIS LENTO CLI IS FOR DEVELOPER USE ONLY. DO NOT
# ATTEMPT TO USE THIS FOR SCRIPTING PURPOSES. END-USER
# USE OF THIS SCRIPT IS NOT SUPPORTED. WE USE THIS 
# SCRIPT FOR LIVE-AMMO TESTING OF THE BACKEND; USING
# IT WITH LENTO MAY HAVE UNINTENDED OR UNEXPECTED
# CONSEQUENCES.
import argparse
import json
from lento.common import cards_management as CardsManagement
from lento import utils

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
    CardsManagement.create_card()
    result_options["output"] = CardsManagement.read_cards()
elif f == "read_cards":
    r = CardsManagement.read_cards()
    result_options["output"] = r
elif f == "delete_card":
    r = CardsManagement.delete_card(param1)
    result_options["output"] = CardsManagement.read_cards()
elif f == "update_metadata":
    r = CardsManagement.update_metadata(param1, param2, param3)
    result_options["output"] = CardsManagement.read_cards()
elif f == "add_to_site_blocklists":
    r = CardsManagement.add_to_site_blocklists(param1, param2, param3)
    result_options["output"] = CardsManagement.read_cards()
elif f == "update_site_blocklists":
    r = CardsManagement.update_site_blocklists(
        param1,
        param2,
        json.loads(param3)
    )
    result_options["output"] = CardsManagement.read_cards()
elif f == "add_to_app_blocklists":
    r = CardsManagement.add_to_app_blocklists(
        param1,
        param2,
        param3.split(",")
    )
    result_options["output"] = CardsManagement.read_cards()
elif f == "get_apps":
    r = utils.get_apps()
elif f == "update_app_blocklists":
    r = CardsManagement.update_app_blocklists(
        param1,
        param2,
        param3,
    )
elif f == "add_notification":
    r = CardsManagement.add_notification(
        param1,
        param2,
        param3,
        param4,
        param5,
        param6,
        param7,
        param8,
        param9,
        param10,
    )
elif f == "update_notification_list":
    r = CardsManagement.update_notification_list(
        param1,
        param2,
    )
elif f == "add_goal":
    r = CardsManagement.add_goal(param1, param2)
elif f == "update_goal_list":
    r = CardsManagement.update_goal_list(param1, param2)
else:
    result_options["message"] = f"INVALID COMMAND: {f}"

print(result_options["message"])
if result_options["output"] is not None:
    print("OUTPUT:")
    print(result_options["output"])
