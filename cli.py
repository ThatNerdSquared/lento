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

args = parser.parse_args()
f = args.name

if f == "create_card":
    cards_management.create_card()
    print("ran create_card successfully!")
else:
    print(f"INVALID COMMAND: {f}")
