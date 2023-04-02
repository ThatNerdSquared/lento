import logging
import json
import platform
from lento.config import Config
import lento.desktop_client.model.block_items as BlockItem

"""
Manages all reading from and writing to lento settings
"""


def activate_card(card_item):
    """
    Mark a provided card item as activated
    """
    settings = json.loads(Config.SETTINGS_PATH.read_text())
    settings["activated_card"] = card_item.id
    Config.SETTINGS_PATH.write_text(json.dumps(settings))


def deactivate_active_card():
    """
    Mark the current activated card as not activated
    """
    settings = json.loads(Config.SETTINGS_PATH.read_text())
    settings["activated_card"] = None
    Config.SETTINGS_PATH.write_text(json.dumps(settings))


def get_activated_card_id():
    """
    Returns the card ID of the current activated card
    """
    settings = json.loads(Config.SETTINGS_PATH.read_text())
    return settings.get("activated_card")


def get_all_card_names():
    """
    Returns a set containing the names of all existing cards
    """
    card_names_set = set()
    settings = json.loads(Config.SETTINGS_PATH.read_text())
    cards_dict = settings.get("cards")

    if cards_dict is None:
        return card_names_set

    # extract each card name and add to set
    for card_id in cards_dict:
        card_dict = cards_dict[card_id]
        card_name = card_dict.get("name")
        if card_name is not None:
            card_names_set.add(card_name)

    return card_names_set


def read_cards():
    """
    Returns a dictionary of LentoCardItem containig all existing cards
    dictionary is of the form { card_id : LentoCardItem }
    """
    cards = {}
    settings = json.loads(Config.SETTINGS_PATH.read_text())
    cards_dict = settings.get("cards")

    if cards_dict is None:
        return cards

    for card_id in cards_dict:
        card_dict = cards_dict[card_id]
        cards[card_id] = get_card(card_dict)

    # write back the settings dictionary since the
    # dictionary may have been modified during reading
    Config.SETTINGS_PATH.write_text(json.dumps(settings))
    return cards


def get_card(card_dict):
    """
    Returns a LentoCardItem built from provided dictionary
    """
    # extract card metadata
    name = card_dict["name"]
    id = card_dict["id"]
    duration = card_dict["duration"]
    end_time = card_dict["end_time"]

    card_item = BlockItem.LentoCardItem(
        id=id, duration=duration, name=name, end_time=end_time
    )

    # build the block items dictionary
    hard_blocked_sites_dict = card_dict.get("hard_blocked_sites", {})
    soft_blocked_sites_dict = card_dict.get("soft_blocked_sites", {})
    hard_blocked_apps_dict = card_dict.get("hard_blocked_apps", {})
    soft_blocked_apps_dict = card_dict.get("soft_blocked_apps", {})

    for label in hard_blocked_sites_dict:
        card_item.block_items[label] = get_website_item(
            label, hard_blocked_sites_dict.get(label), softblock=False
        )

    for label in soft_blocked_sites_dict:
        card_item.block_items[label] = get_website_item(
            label, soft_blocked_sites_dict.get(label), softblock=True
        )

    for label in hard_blocked_apps_dict:
        card_item.block_items[label] = get_app_item(
            label, hard_blocked_apps_dict.get(label), softblock=False
        )

    for label in soft_blocked_apps_dict:
        card_item.block_items[label] = get_app_item(
            label, soft_blocked_apps_dict.get(label), softblock=True
        )

    # mark the card item as saved since we just
    # read the card item from lento settings
    card_item.saved = True

    return card_item


def update_card(card_item):
    """
    Save the provided card item to lento settings
    """
    settings = json.loads(Config.SETTINGS_PATH.read_text())
    cards = settings.get("cards")

    if cards is None:
        raise Exception("No cards in settings config")

    logging.info("Updating card {} in lento settings".format(card_item.id))

    card = cards.setdefault(card_item.id, {})
    card.setdefault("hard_blocked_sites", {})
    card.setdefault("soft_blocked_sites", {})
    card.setdefault("hard_blocked_apps", {})
    card.setdefault("soft_blocked_apps", {})

    # update card metadata
    card["name"] = card_item.name
    card["id"] = card_item.id
    card["duration"] = card_item.duration
    card["end_time"] = card_item.end_time

    # update each block item
    for block_item in card_item.block_items:
        if isinstance(block_item, BlockItem.LentoWebsiteItem):
            list_key = "hard_blocked_sites"
            if block_item.softblock:
                list_key = "soft_blocked_sites"
            card[list_key].update(get_website_dict(block_item))

        elif isinstance(block_item, BlockItem.LentoAppItem):
            list_key = "hard_blocked_apps"
            if not block_item.softblock:
                list_key = "soft_blocked_apps"
            card[list_key].update(get_app_dict(block_item))

    Config.SETTINGS_PATH.write_text(json.dumps(settings))


def get_card_dict(card_item):
    """
    Fetch card dictionary from card item
    """
    settings = json.loads(Config.SETTINGS_PATH.read_text())
    cards = settings.get("cards")

    if cards is None:
        raise Exception("No cards in settings config")

    card_dict = cards.get(card_item.id)

    if card_dict is None:
        return card_dict

    # convert "popup_id" field to "popup_msg" for each block item
    hard_blocked_sites_dict = card_dict.get("hard_blocked_sites", {})
    soft_blocked_sites_dict = card_dict.get("soft_blocked_sites", {})
    hard_blocked_apps_dict = card_dict.get("hard_blocked_apps", {})
    soft_blocked_apps_dict = card_dict.get("soft_blocked_apps", {})

    # iterate the block item dictionaries
    for block_items_dict in [
        hard_blocked_sites_dict,
        soft_blocked_sites_dict,
        hard_blocked_apps_dict,
        soft_blocked_apps_dict,
    ]:
        for item_label in block_items_dict:
            block_item_dict = block_items_dict.get(item_label)
            popup_id = block_item_dict.get("popup_id")
            popup_msg = ""
            # if the block item has a popup ID, fetch
            # the popup item and assign the custom
            # popup msg in "popup_msg" field
            if popup_id != "":
                try:
                    popup_item = get_popup_item(popup_id)
                    popup_msg = popup_item.msg
                except Exception:
                    popup_msg = ""
            block_item_dict["popup_msg"] = popup_msg

    return card_dict


def update_card_metadata(card_item):
    """
    Save the metadata information of a card item
    """
    settings = json.loads(Config.SETTINGS_PATH.read_text())
    cards = settings.get("cards")

    if cards is None:
        raise Exception("No cards in settings config")

    logging.info("Updating metadata for card {} in lento settings".format(card_item.id))

    # crate the block item dictionaries
    card = cards.setdefault(card_item.id, {})
    card.setdefault("hard_blocked_sites", {})
    card.setdefault("soft_blocked_sites", {})
    card.setdefault("hard_blocked_apps", {})
    card.setdefault("soft_blocked_apps", {})

    # update card metadata
    card["name"] = card_item.name
    card["id"] = card_item.id
    card["duration"] = card_item.duration
    card["end_time"] = card_item.end_time

    Config.SETTINGS_PATH.write_text(json.dumps(settings))


def delete_card(card_item):
    """
    Delete card item data from lento settings
    """
    settings = json.loads(Config.SETTINGS_PATH.read_text())

    if settings.get("cards") is None:
        return

    logging.info("Removing card {} from lento settings".format(card_item.id))

    # delete card dictionary with ID
    del settings["cards"][card_item.id]

    Config.SETTINGS_PATH.write_text(json.dumps(settings))


def get_app_item(app_label, app_dict, softblock=False):
    """
    Parameters:
    app_label: label for the app item
    app_dict: app dictionary containing all app information
    softblock: whether the app item is softblocked

    Returns:
    LentoAppItem built from input app dictionary
    """
    # extract app info from app dictionary
    app_path = app_dict["path"]
    icon_path = app_dict["icon_path"]
    allow_interval = app_dict["allow_interval"]
    bundle_id = app_dict.get("bundle_id")
    popup_id = app_dict.get("popup_id")
    popup_item = None

    if len(icon_path) == 0:
        icon_path = None

    # get the popup item from popup id
    if len(popup_id) != 0:
        try:
            popup_item = get_popup_item(popup_id)
        except Exception:
            # if popup item with popup ID does not exist,
            # clear the popup ID in lento settings
            logging.info(
                "Failed to find popup with ID: {} for item {}".format(
                    popup_id, app_path
                )
            )
            popup_item = None
            app_dict["popup_id"] = ""

    # create app item object
    app_item = BlockItem.LentoAppItem(
        app_path,
        softblock=softblock,
        popup_item=popup_item,
        allow_interval=allow_interval,
        load=False,
    )

    app_item.app_bundle_id = bundle_id
    app_item.label = app_label
    app_item.icon_path = icon_path

    return app_item


def save_app_item(card_item, app_item):
    """
    Save an app item object to lento settings
    """
    settings = json.loads(Config.SETTINGS_PATH.read_text())
    cards = settings.get("cards")

    if cards is None:
        raise Exception("No cards in settings config")

    card = cards.get(card_item.id)

    if card is None:
        raise Exception("No card with id {} in" " settings config".format(card_item.id))

    logging.info(
        "Saving app item {} under card {}".format(app_item.label, card_item.id)
    )

    # determine which dictionary this app item should
    # be saved in
    list_key = "hard_blocked_apps"
    if app_item.softblock:
        list_key = "soft_blocked_apps"

    # update the card dictionary with app item dictionary
    card.setdefault(list_key, {})
    card[list_key].update(get_app_dict(app_item))

    Config.SETTINGS_PATH.write_text(json.dumps(settings))


def get_app_dict(app_item):
    """
    Convert an app item into lento settings dictionary
    """
    app_dict = {}
    app_dict[app_item.label] = {}
    app_dict[app_item.label]["enabled"] = True
    app_dict[app_item.label]["path"] = app_item.app_path

    # set "popup_id" field
    if app_item.popup_item:
        app_dict[app_item.label]["popup_id"] = app_item.popup_item.id
    else:
        app_dict[app_item.label]["popup_id"] = ""

    # set "allow_interval" field
    if app_item.softblock:
        app_dict[app_item.label]["allow_interval"] = app_item.allow_interval
    else:
        app_dict[app_item.label]["allow_interval"] = 0

    # set "icon_path" field
    if app_item.icon_path:
        app_dict[app_item.label]["icon_path"] = app_item.icon_path
    else:
        app_dict[app_item.label]["icon_path"] = ""

    # set "bundle_id" for macOS
    current_os = platform.system()
    if current_os == "Darwin":
        app_dict[app_item.label]["bundle_id"] = app_item.app_bundle_id

    return app_dict


def delete_app_item(card_item, app_item):
    """
    Deletes an app item from lento settings
    """
    settings = json.loads(Config.SETTINGS_PATH.read_text())

    if settings.get("cards") is None:
        return

    if settings.get("cards").get(card_item.id) is None:
        return

    logging.info(
        "Deleting app item {} from card {}".format(app_item.label, card_item.id)
    )

    # determine which dictionary this app item exists in
    list_key = "hard_blocked_apps"
    if app_item.softblock:
        list_key = "soft_blocked_apps"

    if settings.get("cards").get(card_item.id).get(list_key) is None:
        return

    # remove the app item from card dictionary
    del settings["cards"][card_item.id][list_key][app_item.label]

    Config.SETTINGS_PATH.write_text(json.dumps(settings))


def get_website_item(website_url, website_dict, softblock=False):
    """
    Parameters:
    website_url: website url for the web item
    website_dict: website dictionary containing all website item info
    softblock: whether the websie item is softblocked

    Returns:
    LentoWebsiteItem built from input website dictionary
    """
    # extract website info from website dictionary
    icon_path = website_dict["icon_path"]
    allow_interval = website_dict["allow_interval"]
    popup_id = website_dict.get("popup_id")

    popup_item = None

    if len(icon_path) == 0:
        icon_path = None

    # get the popup item from popup id
    if len(popup_id) != 0:
        try:
            popup_item = get_popup_item(popup_id)
        except Exception:
            logging.info(
                "Failed to find popup with ID: {} for item {}".format(
                    popup_id, website_url
                )
            )
            popup_item = None
            website_dict["popup_id"] = ""

    # create the website item object
    website_item = BlockItem.LentoWebsiteItem(
        website_url,
        softblock=softblock,
        popup_item=popup_item,
        allow_interval=allow_interval,
    )

    website_item.icon_path = icon_path

    return website_item


def save_website_item(card_item, website_item):
    """
    Save an website item object to lento settings
    """
    settings = json.loads(Config.SETTINGS_PATH.read_text())
    cards = settings.get("cards")

    if cards is None:
        raise Exception("No cards in settings config")

    card = cards.get(card_item.id)

    if card is None:
        raise Exception("No card with id {} in settings config".format(card_item.id))

    logging.info(
        "Saving website item {} under card {}".format(website_item.label, card_item.id)
    )

    # determine which dictionary this website item should
    # be saved in
    list_key = "hard_blocked_sites"
    if website_item.softblock:
        list_key = "soft_blocked_sites"

    # update the card dictionary with website item dictionary
    card.setdefault(list_key, {})
    card[list_key].update(get_website_dict(website_item))

    Config.SETTINGS_PATH.write_text(json.dumps(settings))


def get_website_dict(website_item):
    """
    Convert an website item into lento settings dictionary
    """
    website_dict = {}
    website_dict[website_item.label] = {}
    website_dict[website_item.label]["enabled"] = True

    # set "popup_id" field
    if website_item.popup_item:
        website_dict[website_item.label]["popup_id"] = website_item.popup_item.id
    else:
        website_dict[website_item.label]["popup_id"] = ""

    # set "allow_interval" field
    if website_item.softblock:
        website_dict[website_item.label]["allow_interval"] = website_item.allow_interval
    else:
        website_dict[website_item.label]["allow_interval"] = 0

    # set "icon_path" field
    if website_item.icon_path:
        website_dict[website_item.label]["icon_path"] = website_item.icon_path
    else:
        website_dict[website_item.label]["icon_path"] = ""

    return website_dict


def delete_website_item(card_item, website_item):
    """
    Deletes an website item from lento settings
    """
    settings = json.loads(Config.SETTINGS_PATH.read_text())

    if settings.get("cards") is None:
        return

    if settings.get("cards").get(card_item.id) is None:
        return

    logging.info(
        "Deleting website item {} from card {}".format(website_item.label, card_item.id)
    )

    # determine which dictionary this website item exists in
    list_key = "hard_blocked_sites"
    if website_item.softblock:
        list_key = "soft_blocked_sites"

    if settings.get("cards").get(card_item.id).get(list_key) is None:
        return

    # remove the website item from card dictionary
    del settings["cards"][card_item.id][list_key][website_item.label]

    Config.SETTINGS_PATH.write_text(json.dumps(settings))


def get_popup_items_list():
    """
    Returns:
    a list of LentoPopUpItem object read from lento settings
    """
    settings = json.loads(Config.SETTINGS_PATH.read_text())
    popup_items = []

    # read popup dictionary and popup order list
    popup_dict = settings.get("popups", {}).get("popup_dict")
    popup_order = settings.get("popups", {}).get("popup_order")

    # add each popup item to the list
    if (popup_dict is not None) and (popup_order is not None):
        for id in popup_order:
            msg = popup_dict.get(id)
            # if a popup ID exists in popup order list
            # but not the popup dictionary, remove it
            # from the popup order list
            if msg is not None:
                popup_items.append(BlockItem.LentoPopUpItem(id=id, msg=msg))
            else:
                logging.info("Popup ID {} have no saved msg, deleting")
                popup_order.remove(id)

    # re-save the read settings in case of modifications
    # during reading
    Config.SETTINGS_PATH.write_text(json.dumps(settings))

    return popup_items


def get_popup_item(popup_id):
    """
    Returns:
    LentoPopUpItem object corresponding to provided popup ID
    """
    settings = json.loads(Config.SETTINGS_PATH.read_text())

    popup_dict = settings.get("popups", {}).get("popup_dict")
    popup_order = settings.get("popups", {}).get("popup_order")

    if popup_id not in popup_order or popup_id not in popup_dict:
        raise Exception("Popup {} does not exist".format(popup_id))

    # build the LentoPopUpItem object and return
    return BlockItem.LentoPopUpItem(id=popup_id, msg=popup_dict[popup_id])


def update_popup(popup_item):
    """
    Updates a popup item in lento settings
    """
    settings = json.loads(Config.SETTINGS_PATH.read_text())

    # if the popup item does not currently exist, add it as
    # a new item in lento settings
    if not _popup_exist(settings, popup_item):
        _add_new_popup(settings, popup_item)
    else:
        logging.info(
            "Updating popup item {} with msg {}".format(popup_item.msg, popup_item.id)
        )
        # update the popup message if the popup item exists
        settings["popups"]["popup_dict"][popup_item.id] = popup_item.msg

    Config.SETTINGS_PATH.write_text(json.dumps(settings))


def delete_popup(popup_item):
    """
    Delete popup item from lento settings
    """
    settings = json.loads(Config.SETTINGS_PATH.read_text())

    logging.info("Removing popup item with ID {}".format(popup_item.id))

    # remove the popup item from both popup order list and
    # popup dictionary
    settings["popups"]["popup_order"].remove(popup_item.id)
    settings["popups"]["popup_dict"].pop(popup_item.id)

    cards = settings.get("cards")

    # clear the "popup_id" field of any block item that
    # has this popup ID
    if cards is not None:
        # iterate through all cards
        for card_id in cards:
            card_dict = cards.get(card_id)
            hard_blocked_sites_dict = card_dict.get("hard_blocked_sites", {})
            soft_blocked_sites_dict = card_dict.get("soft_blocked_sites", {})
            hard_blocked_apps_dict = card_dict.get("hard_blocked_apps", {})
            soft_blocked_apps_dict = card_dict.get("soft_blocked_apps", {})

            # for each card, iterate the block item dictionaries
            for block_items_dict in [
                hard_blocked_sites_dict,
                soft_blocked_sites_dict,
                hard_blocked_apps_dict,
                soft_blocked_apps_dict,
            ]:
                # get each block item from each dictionary
                for item_label in block_items_dict:
                    block_item_dict = block_items_dict.get(item_label)
                    popup_id = block_item_dict.get("popup_id")

                    # if the block item has the popup ID to be deleted,
                    # set the block item's popup ID to ""
                    if popup_id is not None and popup_id == popup_item.id:
                        logging.info(
                            "Removing popup id {} from item {} "
                            "in card {}".format(popup_id, item_label, card_id)
                        )
                        block_item_dict["popup_id"] = ""

    Config.SETTINGS_PATH.write_text(json.dumps(settings))


def _popup_exist(settings, popup_item):
    """
    Returns:
    True if the popup item exists in lento settings
    False otherwise
    """
    popup_order = settings.get("popups", {}).get("popup_order")
    if popup_order is None:
        return False
    return popup_item.id in popup_order


def _add_new_popup(settings, popup_item):
    """
    Adds a new popup item to the provided settings dictionary
    """
    # create dictionary under "popups" field if none exist
    if "popups" not in settings.keys():
        settings["popups"] = {}

    # create empty popup dictionary if none exist
    if "popup_dict" not in settings["popups"].keys():
        settings["popups"]["popup_dict"] = {}

    # create empty popup order list if none exist
    if "popup_order" not in settings["popups"].keys():
        settings["popups"]["popup_order"] = []

    logging.info(
        "Adding new popup item id:{} msg:{}".format(popup_item.id, popup_item.msg)
    )

    # add the popup item in popup order list and dictionary
    settings["popups"]["popup_dict"][popup_item.id] = popup_item.msg
    settings["popups"]["popup_order"].append(popup_item.id)
