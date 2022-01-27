# THIS LENTO CLI IS FOR DEVELOPER USE ONLY. DO NOT
# ATTEMPT TO USE THIS FOR SCRIPTING PURPOSES. END-USER
# USE OF THIS SCRIPT IS NOT SUPPORTED. WE USE THIS 
# SCRIPT FOR LIVE-AMMO TESTING OF THE BACKEND; USING
# IT WITH LENTO MAY HAVE UNINTENDED OR UNEXPECTED
# CONSEQUENCES.
import argparse
from lento.common import cards_management

parser = argparse.ArgumentParser(
    description="Run backend functions to make sure they work."
)
parser.add_argument(
    "name",
    type=str,
    help="name of function to run"
)
parser.add_argument(
    "param1",
    nargs='?',
    const='arg_was_not_given',
    help='param for function to run'
)
parser.add_argument(
    "param2",
    nargs='?',
    const='arg_was_not_given',
    help='param for function to run'
)
parser.add_argument(
    "param3",
    nargs='?',
    const='arg_was_not_given',
    help='param for function to run'
)


args = parser.parse_args()
f = args.name
param = args.param1
param2 = args.param2
param3 = args.param3

result_options = {
    "message": f"ran {f} successfully!",
    "output": None,
}

if f == "create_card":
    cards_management.create_card()
    result_options["output"] = cards_management.read_cards()
elif f == "read_cards":
    r = cards_management.read_cards()
    result_options["output"] = r
elif f == "delete_card":
    r = cards_management.delete_card(param)
    result_options["output"] = cards_management.read_cards()
elif f == "update_metadata":
    r = cards_management.update_metadata(param, param2, param3)
    result_options["output"] = cards_management.read_cards()
elif f == "update_site_blocklist":
    r = cards_management.update_site_blocklists(param, param2, param3)
    result_options["output"] = cards_management.read_cards()
else:
    result_options["message"] = f"INVALID COMMAND: {f}"

print(result_options["message"])
if result_options["output"] is not None:
    print("OUTPUT:")
    print(result_options["output"])
