# Lento

## Features
- block websites for certain amount of time
- block apps for certain amount of time
- "sessions": easily block/allow groups of apps/features
- ability to schedule sessions for certain times
- show HUD with session goal when switching apps/idle
- dim non-focused windows

## Technical Details

### Notes
- needs to have a kill switch for safety purposes
- make impervious to date/time changes??
- JSON file with the settings
    - can be reopened from settings
- separate CLI from GUI

### Splitting Responsibilities
- GUI:
    - minimalist but beautiful front-end for the CLI
    - card-like UI interaction?
    - allows users to use the app without being smart enough to break it
    - packaged as platform-specific bundle
- CLI:
    - handles the business logic of the app
    - manages block-lists, places/removes block guardrails, activating/deactivating daemon, error recovery, grabs data
    - packaged as binary bundled with GUI
- Daemon:
    - handles the long-running processes of the app
    - monitors for apps opening, kills apps, starts/stops block timers
    - packaged as binary bundled with GUI

### Blocking
- How do you block websites?
    - common: /etc/hosts
        - vulnerable to DNS-over-HTTPS
    - macOS: pf firewall
    - Windows: Windows firewall via Powershell
- How do you block apps?
    - macOS: daemon via launchd + NSWorkspaceWillLaunchApplicationNotification
        - PyObjC package will allow hooking into this
    - Windows: daemon via Windows Services through Powershell + repeatedly checking to kill
- How do you make the blocklist un-modifiable, during blocks or otherwise?
    - use `cryptography` library and Fernet to encrypt the blocklist
        - not foolproof but will probably deter the average user
    - will be stored as a JSON file before encryption
        - make the CLI check for block-auth before making list changes
- How do you implement soft-blocks?
    - get daemon to poll `netstat` every second and auto-block on first connection, before prompting a GUI popup

### Daemon Logistics
- How do you recover the daemon if killed/make the daemon un-killable?
    - you don't, the user just gets permanently locked 👀 👀 👀
        - have a recovery mode when the app is opened to recover when a daemon is killed
- How do you run a Python program as a daemon/build a daemon in Python?
    - macOS: `python-daemon` package OR launchctl + plist

### Packaging
- How are we packaging up the app?
    - PyInstaller, run on each platform
    - Possibly set up CI for this

### Technologies
- PySide/QT (GUI)
- pf firewall/Windows Firewall (blocking IPs)
- PyObjC (monitoring for app launches, macOS)
- launchd (running as background process, macOS)
- Windows services via Powershell (running as background process, Windows)
- PyInstaller (packaging + binaries)

## Superseding these Apps:
- [SelfControl](http://selfcontrolapp.com)
- [Serene](https://sereneapp.com/#1581441799784-6afc0abc-409e)
- [Monofocus](https://monofocus.app)
- [HazeOver: Distraction Dimmer™ for Productivity on Mac](https://hazeover.com)

## Links
[Moved these to my Raindrop.io collection.](https://raindrop.io/ThatNerd/lento-21974083)
