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


args = parser.parse_args()
f = args.name
param = args.param1

result_options = {
    "message": f"ran {f} successfully!",
    "output": None,
}

if f == "create_card":
    cards_management.create_card()
elif f == "read_cards":
    r = cards_management.read_cards()
    result_options["output"] = r
elif f == "delete_card":
    r = cards_management.delete_card(param)
    result_options["output"] = cards_management.read_cards()
else:
    result_options["message"] = f"INVALID COMMAND: {f}"

print(result_options["message"])
if result_options["output"] is not None:
    print("OUTPUT:")
    print(result_options["output"])
