# flake8: noqa
import os
import textwrap
from lento.config import Config

data = {
    "initial_blank_config": {
        "activated_card": None,
        "cards": {},
        "application_settings": {
            "theme": "automatic"
        }
    },
    "bare_config": {
        "activated_card": None,
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
                "goals": {}
            }
        },
        "application_settings": {
            "theme": "automatic"
        }
    },
    "filled_config":  {
        "activated_card": None,
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
                "goals": {}
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
                "goals": {"Obtain llama": True}
            }
        },
        "application_settings": {
            "theme": "automatic"
        }
    },
    "updated_bare_config": {
        "activated_card": None,
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
                "goals": {}
            }
        },
        "application_settings": {
            "theme": "automatic"
        }
    },
    "bare_config_with_blocked_sites": {
        "activated_card": None,
        "cards": {
            "Untitled Card": {
                "id": "b0244f7e-8369-49f9-89b4-73811eba3a0e",
                "name": "Untitled Card",
                "emoji": "😃",
                "time": 0,
                "hard_blocked_sites": {
                    "youtube.com": True,
                    "twitter.com": True
                },
                "soft_blocked_sites": {},
                "hard_blocked_apps": {},
                "soft_blocked_apps": {},
                "notifications": {},
                "goals": {}
            }
        },
        "application_settings": {
            "theme": "automatic"
        }
    },
    "bare_config_with_sb_sites": {
        "activated_card": None,
        "cards": {
            "Untitled Card": {
                "id": "b0244f7e-8369-49f9-89b4-73811eba3a0e",
                "name": "Untitled Card",
                "emoji": "😃",
                "time": 0,
                "hard_blocked_sites": {},
                "soft_blocked_sites": {
                    "youtube.com": True,
                    "twitter.com": True
                },
                "hard_blocked_apps": {},
                "soft_blocked_apps": {},
                "notifications": {},
                "goals": {}
            }
        },
        "application_settings": {
            "theme": "automatic"
        }
    },
    "bare_config_with_all_blocked_sites": {
        "activated_card": None,
        "cards": {
            "Untitled Card": {
                "id": "b0244f7e-8369-49f9-89b4-73811eba3a0e",
                "name": "Untitled Card",
                "emoji": "😃",
                "time": 0,
                "hard_blocked_sites": {
                    "youtube.com": True,
                    "twitter.com": True
                },
                "soft_blocked_sites": {
                    "discord.com": True,
                    "slack.com": True
                },
                "hard_blocked_apps": {},
                "soft_blocked_apps": {},
                "notifications": {},
                "goals": {}
            }
        },
        "application_settings": {
            "theme": "automatic"
        }
    },
    "bare_config_with_apps": {
        "activated_card": None,
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
                "goals": {}
            }
        },
        "application_settings": {
            "theme": "automatic"
        }
    },
    "bare_config_reordered_apps": {
        "activated_card": None,
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
                "goals": {}
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
        "activated_card": None,
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
                "goals": {}
            }
        },
        "application_settings": {
            "theme": "automatic"
        }
    },
    "bare_config_multiple_notif": {
        "activated_card": None,
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
                    },
                    "2d189b37-6eaf-478f-a5ab-e19c9dab5738": {
                        "name": "Test Notif 2",
                        "enabled": False,
                        "type": "popup",
                        "blocked_visit_triggers": [],
                        "associated_goals": [
                            "Create pet AI"
                        ],
                        "time_interval_trigger": 900000,
                        "title": "Work on %g",
                        "body": "Keep focused!",
                        "audio_paths": {
                            "Bloop": "/System/Library/Sounds/Bloop.aiff"
                        }
                    }
                },
                "goals": {}
            }
        },
        "application_settings": {
            "theme": "automatic"
        }
    },
    "GRIS": textwrap.dedent("""
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        <dict>
            <key>NSAppTransportSecurity</key>
            <dict>
                <key>NSAllowsArbitraryLoads</key>
                <true/>
            </dict>
            <key>CFBundleDevelopmentRegion</key>
            <string>English</string>
            <key>CFBundleExecutable</key>
            <string>GRIS</string>
            <key>CFBundleGetInfoString</key>
            <string>Unity Player version 2017.4.10f1 (f2cce2a5991f). (c) 2018 Unity Technologies ApS. All rights reserved.</string>
            <key>CFBundleIconFile</key>
            <string>PlayerIcon.icns</string>
            <key>CFBundleIdentifier</key>
            <string>unity.nomada studio.GRIS</string>
            <key>CFBundleInfoDictionaryVersion</key>
            <string>6.0</string>
            <key>CFBundleSupportedPlatforms</key>
                <array>
                    <string>MacOSX</string>
                </array>
            <key>LSApplicationCategoryType</key>
            <string>public.app-category.games</string>
            <key>CFBundleName</key>
            <string>GRIS</string>
            <key>CFBundlePackageType</key>
            <string>APPL</string>
            <key>CFBundleShortVersionString</key>
            <string>1.0</string>
            <key>CFBundleVersion</key>
            <string>0</string>
            <key>NSMainNibFile</key>
            <string>MainMenu</string>
            <key>NSPrincipalClass</key>
            <string>PlayerApplication</string>
            <key>UnityBuildNumber</key>
            <string>f2cce2a5991f</string>
            <key>LSMinimumSystemVersion</key>
            <string>10.9.0</string>
        </dict>
        </plist>
    """).strip(),
    "Scrivener": textwrap.dedent("""
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        <dict>
            <key>ATSApplicationFontsPath</key>
            <string>Fonts</string>
            <key>BuildMachineOSBuild</key>
            <string>20B29</string>
            <key>CFBundleDevelopmentRegion</key>
            <string>English</string>
            <key>CFBundleDocumentTypes</key>
            <array>
                <dict>
                    <key>CFBundleTypeExtensions</key>
                    <array>
                        <string>scrivx</string>
                    </array>
                    <key>CFBundleTypeIconFile</key>
                    <string>ScrivenerXML</string>
                    <key>CFBundleTypeName</key>
                    <string>Scrivener XML document</string>
                    <key>CFBundleTypeOSTypes</key>
                    <array>
                        <string>scrivx</string>
                    </array>
                    <key>CFBundleTypeRole</key>
                    <string>Viewer</string>
                    <key>LSHandlerRank</key>
                    <string>Owner</string>
                    <key>LSTypeIsPackage</key>
                    <false/>
                    <key>NSDocumentClass</key>
                    <string>SCRMainDocument</string>
                    <key>NSPersistentStoreTypeKey</key>
                    <string>XML</string>
                </dict>
                <dict>
                    <key>CFBundleTypeExtensions</key>
                    <array>
                        <string>scriv</string>
                    </array>
                    <key>CFBundleTypeIconFile</key>
                    <string>ScrivenerDocument</string>
                    <key>CFBundleTypeName</key>
                    <string>Scrivener Project</string>
                    <key>CFBundleTypeOSTypes</key>
                    <array>
                        <string>scriv</string>
                    </array>
                    <key>CFBundleTypeRole</key>
                    <string>Editor</string>
                    <key>LSHandlerRank</key>
                    <string>Owner</string>
                    <key>LSTypeIsPackage</key>
                    <string>YES</string>
                    <key>NSDocumentClass</key>
                    <string>SCRMainDocument</string>
                    <key>NSPersistentStoreTypeKey</key>
                    <string>Binary</string>
                </dict>
                <dict>
                    <key>CFBundleTypeExtensions</key>
                    <array>
                        <string>scrivtemplate</string>
                    </array>
                    <key>CFBundleTypeIconFile</key>
                    <string>ScrivenerTemplate</string>
                    <key>CFBundleTypeName</key>
                    <string>Scrivener Template</string>
                    <key>CFBundleTypeRole</key>
                    <string>None</string>
                    <key>LSHandlerRank</key>
                    <string>Owner</string>
                    <key>NSDocumentClass</key>
                    <string>SCRMainDocument</string>
                </dict>
                <dict>
                    <key>CFBundleTypeExtensions</key>
                    <array>
                        <string>scrformat</string>
                    </array>
                    <key>CFBundleTypeIconFile</key>
                    <string>CompileFormat</string>
                    <key>CFBundleTypeMIMETypes</key>
                    <array/>
                    <key>CFBundleTypeName</key>
                    <string>Scrivener Compile Format</string>
                    <key>CFBundleTypeRole</key>
                    <string>None</string>
                    <key>LSHandlerRank</key>
                    <string>Owner</string>
                    <key>LSTypeIsPackage</key>
                    <integer>0</integer>
                    <key>NSDocumentClass</key>
                    <string>SCRMainDocument</string>
                </dict>
            </array>
            <key>CFBundleExecutable</key>
            <string>Scrivener</string>
            <key>CFBundleHelpBookFolder</key>
            <string>Help</string>
            <key>CFBundleHelpBookName</key>
            <string>Scrivener Help</string>
            <key>CFBundleIconFile</key>
            <string>Scrivener</string>
            <key>CFBundleIconName</key>
            <string>Scrivener</string>
            <key>CFBundleIdentifier</key>
            <string>com.literatureandlatte.scrivener3</string>
            <key>CFBundleInfoDictionaryVersion</key>
            <string>6.0</string>
            <key>CFBundleName</key>
            <string>Scrivener</string>
            <key>CFBundlePackageType</key>
            <string>APPL</string>
            <key>CFBundleShortVersionString</key>
            <string>3.2.2</string>
            <key>CFBundleSignature</key>
            <string>Scrv</string>
            <key>CFBundleSupportedPlatforms</key>
            <array>
                <string>MacOSX</string>
            </array>
            <key>CFBundleURLTypes</key>
            <array>
                <dict>
                    <key>CFBundleTypeRole</key>
                    <string>Editor</string>
                    <key>CFBundleURLName</key>
                    <string>Scrivener Reference</string>
                    <key>CFBundleURLSchemes</key>
                    <array>
                        <string>x-scrivener-item</string>
                    </array>
                    <key>LSIsAppleDefaultForScheme</key>
                    <true/>
                </dict>
            </array>
            <key>CFBundleVersion</key>
            <string>14632</string>
            <key>DTCompiler</key>
            <string>com.apple.compilers.llvm.clang.1_0</string>
            <key>DTPlatformBuild</key>
            <string>12B45b</string>
            <key>DTPlatformName</key>
            <string>macosx</string>
            <key>DTPlatformVersion</key>
            <string>11.0</string>
            <key>DTSDKBuild</key>
            <string>20A2408</string>
            <key>DTSDKName</key>
            <string>macosx11.0</string>
            <key>DTXcode</key>
            <string>1220</string>
            <key>DTXcodeBuild</key>
            <string>12B45b</string>
            <key>LSApplicationCategoryType</key>
            <string>public.app-category.productivity</string>
            <key>LSMinimumSystemVersion</key>
            <string>10.12</string>
            <key>NSAccentColorName</key>
            <string>AccentColor</string>
            <key>NSAppTransportSecurity</key>
            <dict>
                <key>NSAllowsArbitraryLoads</key>
                <true/>
            </dict>
            <key>NSAppleEventsUsageDescription</key>
            <string>Scrivener uses Apple Events to communicate with MathType for inserting equations, for receiving text from bibliography managers, and to allow quick access to the system's text preferences.</string>
            <key>NSHumanReadableCopyright</key>
            <string>Â© Literature &amp; Latte 2005-2020</string>
            <key>NSMainNibFile</key>
            <string>MainMenu</string>
            <key>NSPrincipalClass</key>
            <string>SCRApplication</string>
            <key>NSServices</key>
            <array>
                <dict>
                    <key>NSMenuItem</key>
                    <dict>
                        <key>default</key>
                        <string>Scrivener/Scrivener: Make New Clipping</string>
                    </dict>
                    <key>NSMessage</key>
                    <string>createClipping</string>
                    <key>NSPortName</key>
                    <string>Scrivener</string>
                    <key>NSSendTypes</key>
                    <array>
                        <string>com.apple.flat-rtfd</string>
                        <string>public.rtf</string>
                        <string>public.utf8-plain-text</string>
                    </array>
                </dict>
                <dict>
                    <key>NSMenuItem</key>
                    <dict>
                        <key>default</key>
                        <string>Scrivener/Scrivener: Make New Clipping (Unformatted)</string>
                    </dict>
                    <key>NSMessage</key>
                    <string>createPlainTextClipping</string>
                    <key>NSPortName</key>
                    <string>Scrivener</string>
                    <key>NSSendTypes</key>
                    <array>
                        <string>com.apple.flat-rtfd</string>
                        <string>public.rtf</string>
                        <string>public.utf8-plain-text</string>
                    </array>
                </dict>
                <dict>
                    <key>NSMenuItem</key>
                    <dict>
                        <key>default</key>
                        <string>Scrivener/Scrivener: Append to Text</string>
                    </dict>
                    <key>NSMessage</key>
                    <string>appendSelection</string>
                    <key>NSPortName</key>
                    <string>Scrivener</string>
                    <key>NSSendTypes</key>
                    <array>
                        <string>com.apple.flat-rtfd</string>
                        <string>public.rtf</string>
                        <string>public.utf8-plain-text</string>
                    </array>
                </dict>
                <dict>
                    <key>NSMenuItem</key>
                    <dict>
                        <key>default</key>
                        <string>Scrivener/Scrivener: Append to Text (Unformatted)</string>
                    </dict>
                    <key>NSMessage</key>
                    <string>appendSelectionAsPlainText</string>
                    <key>NSPortName</key>
                    <string>Scrivener</string>
                    <key>NSSendTypes</key>
                    <array>
                        <string>com.apple.flat-rtfd</string>
                        <string>public.rtf</string>
                        <string>public.utf8-plain-text</string>
                    </array>
                </dict>
                <dict>
                    <key>NSMenuItem</key>
                    <dict>
                        <key>default</key>
                        <string>Scrivener/Scrivener: Append to Notes</string>
                    </dict>
                    <key>NSMessage</key>
                    <string>appendSelectionToNotes</string>
                    <key>NSPortName</key>
                    <string>Scrivener</string>
                    <key>NSSendTypes</key>
                    <array>
                        <string>com.apple.flat-rtfd</string>
                        <string>public.rtf</string>
                        <string>public.utf8-plain-text</string>
                    </array>
                </dict>
                <dict>
                    <key>NSMenuItem</key>
                    <dict>
                        <key>default</key>
                        <string>Scrivener/Scrivener: Append to Notes (Unformatted)</string>
                    </dict>
                    <key>NSMessage</key>
                    <string>appendSelectionToNotesAsPlainText</string>
                    <key>NSPortName</key>
                    <string>Scrivener</string>
                    <key>NSSendTypes</key>
                    <array>
                        <string>com.apple.flat-rtfd</string>
                        <string>public.rtf</string>
                        <string>public.utf8-plain-text</string>
                    </array>
                </dict>
            </array>
            <key>NSSupportsAutomaticGraphicsSwitching</key>
            <true/>
            <key>NSSupportsSuddenTermination</key>
            <true/>
            <key>SUFeedURL</key>
            <string>https://www.literatureandlatte.com/downloads/scrivener-3.xml</string>
            <key>SUPublicDSAKeyFile</key>
            <string>dsa_pub.pem</string>
            <key>UTExportedTypeDeclarations</key>
            <array>
                <dict>
                    <key>UTTypeConformsTo</key>
                    <array>
                        <string>public.xml</string>
                    </array>
                    <key>UTTypeDescription</key>
                    <string>Scrivener Compile Format</string>
                    <key>UTTypeIconFile</key>
                    <string>CompileFormat</string>
                    <key>UTTypeIdentifier</key>
                    <string>com.literatureandlatte.scrformat</string>
                    <key>UTTypeTagSpecification</key>
                    <dict>
                        <key>public.filename-extension</key>
                        <array>
                            <string>scrformat</string>
                        </array>
                    </dict>
                </dict>
            </array>
        </dict>
        </plist>
    """).strip(),
    "NetNewsWire": textwrap.dedent("""
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        <dict>
            <key>AppGroup</key>
            <string>group.com.ranchero.NetNewsWire-Evergreen</string>
            <key>AppIdentifierPrefix</key>
            <string>M8L2WTLA8W.</string>
            <key>BuildMachineOSBuild</key>
            <string>20D91</string>
            <key>CFBundleDevelopmentRegion</key>
            <string>en</string>
            <key>CFBundleExecutable</key>
            <string>NetNewsWire</string>
            <key>CFBundleIconFile</key>
            <string>AppIcon</string>
            <key>CFBundleIconName</key>
            <string>AppIcon</string>
            <key>CFBundleIdentifier</key>
            <string>com.ranchero.NetNewsWire-Evergreen</string>
            <key>CFBundleInfoDictionaryVersion</key>
            <string>6.0</string>
            <key>CFBundleName</key>
            <string>NetNewsWire</string>
            <key>CFBundlePackageType</key>
            <string>APPL</string>
            <key>CFBundleShortVersionString</key>
            <string>6.0.2</string>
            <key>CFBundleSupportedPlatforms</key>
            <array>
                <string>MacOSX</string>
            </array>
            <key>CFBundleURLTypes</key>
            <array>
                <dict>
                    <key>CFBundleTypeRole</key>
                    <string>Viewer</string>
                    <key>CFBundleURLName</key>
                    <string>RSS Feed</string>
                    <key>CFBundleURLSchemes</key>
                    <array>
                        <string>feed</string>
                        <string>feeds</string>
                    </array>
                </dict>
            </array>
            <key>CFBundleVersion</key>
            <string>6032</string>
            <key>DTCompiler</key>
            <string>com.apple.compilers.llvm.clang.1_0</string>
            <key>DTPlatformBuild</key>
            <string>12D4e</string>
            <key>DTPlatformName</key>
            <string>macosx</string>
            <key>DTPlatformVersion</key>
            <string>11.1</string>
            <key>DTSDKBuild</key>
            <string>20C63</string>
            <key>DTSDKName</key>
            <string>macosx11.1</string>
            <key>DTXcode</key>
            <string>1240</string>
            <key>DTXcodeBuild</key>
            <string>12D4e</string>
            <key>DeveloperEntitlements</key>
            <string></string>
            <key>FeedURLForTestBuilds</key>
            <string>https://ranchero.com/downloads/netnewswire-beta.xml</string>
            <key>LSApplicationCategoryType</key>
            <string>public.app-category.news</string>
            <key>LSMinimumSystemVersion</key>
            <string>10.15</string>
            <key>NSAccentColorName</key>
            <string>AccentColor</string>
            <key>NSAppTransportSecurity</key>
            <dict>
                <key>NSAllowsArbitraryLoads</key>
                <true/>
            </dict>
            <key>NSAppleEventsUsageDescription</key>
            <string>NetNewsWire communicates with other apps on your Mac when you choose to share an article.</string>
            <key>NSAppleScriptEnabled</key>
            <true/>
            <key>NSHumanReadableCopyright</key>
            <string>Copyright Â© 2002-2021 Brent Simmons. All rights reserved.</string>
            <key>NSMainStoryboardFile</key>
            <string>Main</string>
            <key>NSPrincipalClass</key>
            <string>NSApplication</string>
            <key>NSUserActivityTypes</key>
            <array>
                <string>ReadArticle</string>
            </array>
            <key>OSAScriptingDefinition</key>
            <string>NetNewsWire.sdef</string>
            <key>OrganizationIdentifier</key>
            <string>com.ranchero</string>
            <key>SUFeedURL</key>
            <string>https://ranchero.com/downloads/netnewswire-release.xml</string>
            <key>UserAgent</key>
            <string>NetNewsWire (RSS Reader; https://netnewswire.com/)</string>
        </dict>
        </plist>
    """).strip(),
    "reordered_notifs_dict": {
        "2d189b37-6eaf-478f-a5ab-e19c9dab5738": {
            "name": "Test Notif 2",
            "enabled": False,
            "type": "popup",
            "blocked_visit_triggers": [],
            "associated_goals": [
                "Create pet AI"
            ],
            "time_interval_trigger": 900000,
            "title": "Work on %g",
            "body": "Keep focused!",
            "audio_paths": {
                "Bloop": "/System/Library/Sounds/Bloop.aiff"
            }
        },
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
    "deleted_notifs_dict": {
        "2d189b37-6eaf-478f-a5ab-e19c9dab5738": {
            "name": "Test Notif 2",
            "enabled": False,
            "type": "popup",
            "blocked_visit_triggers": [],
            "associated_goals": [
                "Create pet AI"
            ],
            "time_interval_trigger": 900000,
            "title": "Work on %g",
            "body": "Keep focused!",
            "audio_paths": {
                "Bloop": "/System/Library/Sounds/Bloop.aiff"
            }
        }
    },
    "flawed_notifs_dict": {
        "2d189b37-6eaf-478f-a5ab-e19c9dab5738": {
            "name": "Test Notif 2",
            "enabled": False,
            "blocked_visit_triggers": [],
            "associated_goals": [
                "Create pet AI"
            ],
            "time_interval_trigger": 900000,
            "title": "Work on %g",
            "body": "Keep focused!",
            "audio_paths": {
                "Bloop": "/System/Library/Sounds/Bloop.aiff"
            }
        }
    },
    "bare_config_with_goals": {
        "activated_card": None,
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
                "goals": {
                    "Debug USACO problem": True,
                    "Conquer world": False
                }
            }
        },
        "application_settings": {
            "theme": "automatic"
        }
    },
    "reordered_goal_dict": {
        "Conquer world": False,
        "Debug USACO problem": True
    },
    "proper_apps_dict": {
        "Trello": {
            "path": str(os.path.join(
                Config.DRIVE_LETTER,
                "Program Files",
                "WindowsApps",
                "45273LiamForsyth.PawsforTrello_2.12.5.0_x64__7pb5ddty8z1pa",
                "app",
                "Trello.exe"
            )),
            "icon_path": str(os.path.join(
                Config.DRIVE_LETTER,
                "Program Files",
                "WindowsApps",
                "45273LiamForsyth.PawsforTrello_2.12.5.0_x64__7pb5ddty8z1pa",
                "assets",
                "Square310x310Logo.scale-200.png"
            ))
        },
        "vivaldi": { }
    },
    "apps_to_add": [
        {
            "name": "Trello",
            "path": str(os.path.join(
                Config.DRIVE_LETTER,
                "Program Files",
                "WindowsApps",
                "45273LiamForsyth.PawsforTrello_2.12.5.0_x64__7pb5ddty8z1pa",
                "app",
                "Trello.exe"
            )),
            "icon_path": str(os.path.join(
                Config.DRIVE_LETTER,
                "Program Files",
                "WindowsApps",
                "45273LiamForsyth.PawsforTrello_2.12.5.0_x64__7pb5ddty8z1pa",
                "assets",
                "Square310x310Logo.scale-200.png"
            ))
        },
        {
            "name": "vivaldi",
        }
    ],
    "expected_pf_anchor": textwrap.dedent("""
        # Options
        set block-policy drop
        set fingerprints "/etc/pf.os"
        set ruleset-optimization basic
        set skip on lo0

        #
        # Rules for Lento blocks
        #
        block return out proto tcp from any to 172.217.14.206
        block return out proto udp from any to 172.217.14.206
        block return out proto tcp from any to 104.244.42.193
        block return out proto udp from any to 104.244.42.193
        rdr pass log on lo0 proto tcp from any to 162.159.138.232 -> 127.0.0.1 port 65531
        rdr pass log on lo0 proto udp from any to 162.159.138.232 -> 127.0.0.1 port 65531
        pass out on en0 route-to lo0 proto tcp from en0 to 162.159.138.232 keep state
        pass out on en0 route-to lo0 proto udp from en0 to 162.159.138.232 keep state
        rdr pass log on lo0 proto tcp from any to 3.95.117.96 -> 127.0.0.1 port 65531
        rdr pass log on lo0 proto udp from any to 3.95.117.96 -> 127.0.0.1 port 65531
        pass out on en0 route-to lo0 proto tcp from en0 to 3.95.117.96 keep state
        pass out on en0 route-to lo0 proto udp from en0 to 3.95.117.96 keep state
    """).lstrip(),
    "expected_pf_conf": textwrap.dedent("""
        #io.github.lento
        anchor "io.github.lento"
        load anchor "io.github.lento" from "/etc/pf.anchors/io.github.lento\"
    """).lstrip(),
    "bare_config_with_activated_card": {
        "activated_card": "Untitled Card",
        "cards": {
            "Untitled Card": {
                "id": "b0244f7e-8369-49f9-89b4-73811eba3a0e",
                "name": "Untitled Card",
                "emoji": "😃",
                "time": 0,
                "hard_blocked_sites": {
                    "youtube.com": True,
                    "twitter.com": True
                },
                "soft_blocked_sites": {},
                "hard_blocked_apps": {},
                "soft_blocked_apps": {},
                "notifications": {},
                "goals": {}
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


class fake_image:
    def convert(x):
        return fake_rgb


class fake_rgb:
    def save(x):
        return True

def fake_subprocess(cmd, shell=True):
    if type(cmd) is list:
        cmd = " ".join(cmd)
    correct_trello_path = "".join([
        str(os.path.join(
            Config.DRIVE_LETTER,
            "Program Files",
            "WindowsApps",
            "45273LiamForsyth.PawsforTrello_2.12.5.0_x64__7pb5ddty8z1pa",
            "app",
            "Trello.exe"
        )),
        "   "
    ])
    correct_vivaldi_path = "".join([
        str(os.path.join(
            os.path.expanduser("~"),
            "AppData",
            "Local",
            "Vivaldi",
            "Application",
            "vivaldi.exe"
        )),
        "   "
    ])
    cases = {
        "powershell \"Get-Process -FileVersionInfo -ErrorAction SilentlyContinue | Select-Object FileName\"": f"""     
FileName   
--------   
{correct_trello_path}
{correct_trello_path}
{correct_vivaldi_path}
{correct_vivaldi_path}""",
        "powershell \"(Get-AppxPackage -Name \"*Trello*\" | Get-AppxPackageManifest).package.applications.application.VisualElements.DefaultTile.Square310x310Logo\"": os.path.join("assets", "Square310x310Logo.png"),
        "powershell \"{Add-Type -AssemblyName System.Drawing\n[System.Drawing.Icon]::ExtractAssociatedIcon(\'{app_path}\').toBitmap().Save(\'{app_icon_path}\')command_string}\"": "",
        "/sbin/pfctl -E -f /etc/pf.conf": "rules_activated",
        "/sbin/pfctl -F rules": "flushed_rules",
        "networksetup -setwebproxy wi-fi localhost 42": "macOS web proxy activated",
        "networksetup -setsecurewebproxy wi-fi localhost 42": "macOS secure web proxy activated",
        "networksetup -setwebproxystate wi-fi off": "macOS web proxy deactivated",
        "networksetup -setsecurewebproxystate wi-fi off": "macOS secure web proxy deactivated",
        f"cp \"lentodaemon\" \"{Config.DAEMON_BINARY_PATH}\"": "macOS daemon copied",
        f"rm -f \"{Config.DAEMON_BINARY_PATH}\"": "macOS block cleanup finished",
        "/tmp/lentodaemon Untitled Card 42": "daemon launched",
        "\\tmp\\lentodaemon Untitled Card 42": "daemon launched",
        "powershell \"cp \"lentodaemon.exe\" \"/tmp/lentodaemon\"\"": "Windows daemon copied",
        "powershell \"cp \"lentodaemon.exe\" \"\\tmp\\lentodaemon\"\"": "Windows daemon copied",
        "powershell \"rm -Force \'/tmp/lentodaemon\'\"": "Windows block cleanup finished",
        "powershell \"rm -Force \'\\tmp\\lentodaemon\'\"": "Windows block cleanup finished"
    }
    return cases[cmd]


def fake_gethost(domain):
    match domain:
        case "youtube.com":
            return "172.217.14.206"
        case "twitter.com":
            return "104.244.42.193"
        case "discord.com":
            return "162.159.138.232"
        case "slack.com":
            return "3.95.117.96"
        case _:
            raise Exception(f"Domain name '{domain}' not found in mock domains match statement!")


def fake_SetValueEx_enable(reg, key, num, type, value):
    match key:
        case "ProxyServer":
            return "proxyserver_command_run"
        case "ProxyEnable":
            return "proxyenable_command_run"
        case _:
            raise Exception(f"Mock return for {key} not found")


def fake_SetValueEx_disable(reg, key, num, type, value):
    match key:
        case "ProxyServer":
            return "proxyserver_removed"
        case "ProxyEnable":
            return "proxyenable_disabled"
        case _:
            raise Exception(f"Mock return for {key} not found")


class FakeSQLite:
    def __init__(self):
        super().__init__()

    def create_tables(self, tables):
        return tables

    def close(self):
        return


class fakeFavicon:
    def grab(self, url):
        return [FakeIcon(url)]

class FakeIcon:
    def __init__(self, url):
        self.data = f"{url}.bytes"
        self.extension = "png"
