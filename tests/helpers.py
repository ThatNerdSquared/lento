data = {
    "initial_blank_config": {
        "is_block_running": False,
        "cards": {},
        "application_settings": {
            "theme": "automatic"
        }
    },
    "bare_config": {
        "is_block_running": False,
        "cards": {
            "Untitled Card": {
                "id": "b0244f7e-8369-49f9-89b4-73811eba3a0e",
                "name": "Untitled Card",
                "emoji": "😃",
                "time": 0,
                "hard_blocked_sites": {},
                "soft_blocked_sites": {},
                "hard_blocked_apps": {},
                "soft_blocked_apps": {},
                "notifications": {},
                "goals": []
            }
        },
        "application_settings": {
            "theme": "automatic"
        }
    },
    "filled_config":  {
        "is_block_running": False,
        "cards": {
            "Untitled Card": {
                "id": "b0244f7e-8369-49f9-89b4-73811eba3a0e",
                "name": "Untitled Card",
                "emoji": "😃",
                "time": 0,
                "hard_blocked_sites": {},
                "soft_blocked_sites": {},
                "hard_blocked_apps": {},
                "soft_blocked_apps": {},
                "notifications": {},
                "goals": []
            },
            "Llama Taming": {
                "id": "e68d8993-ee30-4e3f-941b-43c074e2759c",
                "name": "Llama Taming",
                "emoji": "🦙",
                "time": 5400,
                "hard_blocked_sites": {
                    "twitter.com": True
                },
                "soft_blocked_sites": {
                    "youtube.com": True
                },
                "hard_blocked_apps": {
                    "NetNewsWire": True
                },
                "soft_blocked_apps": {
                    "calibre": False
                },
                "notifications": {
                    "2d189b37-6eaf-478f-a5ab-e19c9dab5738": {
                        "name": "Test Notif 1",
                        "enabled": True,
                        "type": "popup",
                        "blocked_visit_triggers": [],
                        "associated_goals": [
                            "Obtain llama"
                        ],
                        "time_interval_trigger": 900000,
                        "title": "Get back to %g!",
                        "body": "Keep focused!",
                        "audio_paths": {
                            "Bloop": "/System/Library/Sounds/Bloop.aiff"
                        }
                    }
                },
                "goals": ["Obtain llama"]
            }
        },
        "application_settings": {
            "theme": "automatic"
        }
    },
    "updated_bare_config": {
        "is_block_running": False,
        "cards": {
            "World Domination": {
                "id": "b0244f7e-8369-49f9-89b4-73811eba3a0e",
                "name": "World Domination",
                "emoji": "😃",
                "time": 0,
                "hard_blocked_sites": {},
                "soft_blocked_sites": {},
                "hard_blocked_apps": {},
                "soft_blocked_apps": {},
                "notifications": {},
                "goals": []
            }
        },
        "application_settings": {
            "theme": "automatic"
        }
    },
    "bare_config_with_apps": {
        "is_block_running": False,
        "cards": {
            "Untitled Card": {
                "id": "b0244f7e-8369-49f9-89b4-73811eba3a0e",
                "name": "Untitled Card",
                "emoji": "😃",
                "time": 0,
                "hard_blocked_sites": {},
                "soft_blocked_sites": {},
                "hard_blocked_apps": {
                    "calibre": {
                        "enabled": False,
                        "bundle_id": "net.kovidgoyal.calibre",
                        "app_icon_path": "~/Library/Application Support/Lento/calibre.jpg"  # noqa: E501
                    },
                    "GRIS": {
                        "enabled": True,
                        "bundle_id": "unity.nomada studio.GRIS",
                        "app_icon_path": "~/Library/Application Support/Lento/GRIS.jpg"  # noqa: E501
                    }
                },
                "soft_blocked_apps": {},
                "notifications": {},
                "goals": []
            }
        },
        "application_settings": {
            "theme": "automatic"
        }
    },
    "bare_config_reordered_apps": {
        "is_block_running": False,
        "cards": {
            "Untitled Card": {
                "id": "b0244f7e-8369-49f9-89b4-73811eba3a0e",
                "name": "Untitled Card",
                "emoji": "😃",
                "time": 0,
                "hard_blocked_sites": {},
                "soft_blocked_sites": {},
                "hard_blocked_apps": {
                    "GRIS": {
                        "enabled": True,
                        "bundle_id": "unity.nomada studio.GRIS",
                        "app_icon_path": "~/Library/Application Support/Lento/GRIS.jpg"  # noqa: E501
                    },
                    "calibre": {
                        "enabled": False,
                        "bundle_id": "net.kovidgoyal.calibre",
                        "app_icon_path": "~/Library/Application Support/Lento/calibre.jpg"  # noqa: E501
                    }
                },
                "soft_blocked_apps": {},
                "notifications": {},
                "goals": []
            }
        },
        "application_settings": {
            "theme": "automatic"
        }
    },
    "new_blocklist": {
        "GRIS": {
            "enabled": True,
            "bundle_id": "unity.nomada studio.GRIS",
            "app_icon_path": "~/Library/Application Support/Lento/GRIS.jpg"
        },
        "calibre": {
            "enabled": False,
            "bundle_id": "net.kovidgoyal.calibre",
            "app_icon_path": "~/Library/Application Support/Lento/calibre.jpg"
        }
    },
    "bare_config_with_notif": {
        "is_block_running": False,
        "cards": {
            "Untitled Card": {
                "id": "b0244f7e-8369-49f9-89b4-73811eba3a0e",
                "name": "Untitled Card",
                "emoji": "😃",
                "time": 0,
                "hard_blocked_sites": {},
                "soft_blocked_sites": {},
                "hard_blocked_apps": {},
                "soft_blocked_apps": {},
                "notifications": {
                    "a019868e-f43f-478f-8dcc-ba78c35525c4": {
                        "name": "Test Notif 1",
                        "enabled": True,
                        "type": "banner",
                        "blocked_visit_triggers": [
                            "youtube.com",
                            "twitter.com"
                        ],
                        "associated_goals": [
                            "Debug USACO problem"
                        ],
                        "time_interval_trigger": None,
                        "title": "Get back to %g!",
                        "body": "Keep focused!",
                        "audio_paths": {
                            "reminder": "~/Desktop/reminder.mp3",
                            "Frog": "/System/Library/Sounds/Frog.aiff"
                        }
                    }
                },
                "goals": []
            }
        },
        "application_settings": {
            "theme": "automatic"
        }
    },
}


def fake_bundle_id(args):
    app = args[-1]
    cases = {
        "/Applications/GRIS.app": b"unity.nomada studio.GRIS",
        "/Applications/Scrivener.app": b"com.literatureandlatte.scrivener3",
        "/Applications/NetNewsWire.app": b"com.ranchero.NetNewsWire-Evergreen"
    }
    return cases[app]
