# Lento

## Features
- multiple cards, each with a goal and blocklist/notification presets
- blocks both apps and websites
- can set time lengths for different goals
- block is hardcore (cannot disable before time runs out )
- "soft block" support (given a prompt when opening app/site instead of outright block)
- block survives across uninstalls/logouts/reboots
- browser agnostic, no extensions required
- advanced notification functionality (remind yourself of goals at set intervals/on idle/when switching apps)
    - different notification types: text, popup, audio message, with optional notification sound
- clean/easy to use UI
- cross-platform (Windows/macOS, Linux support coming soon)
- free, open source

## Technical Details

### The Different Parts
- GUI:
    - minimalist but beautiful front-end for the CLI
    - card-like UI interaction?
    - allows users to use the app without being smart enough to break it
    - packaged as platform-specific bundle
- Common:
    - backend, used with both GUI and daemon
    - handles the business logic of the app
    - manages cards/blocklists/notifications, places/removes block guardrails, activates/deactivates daemon, error recovery
    - packaged with both GUI and daemon
- Daemon:
    - handles the long-running processes of the app
    - monitors for apps opening, kills apps, starts/stops block timers, handles notifications, sets watchers for critical system files, manages softblocks
    - packaged as binary bundled with GUI
- Utils:
    - set of functions that are used in various places across the codebase
    - separated to avoid repetition
    - packaged wherever used

### Blocking
- How do you hard-block websites?
    - common: /etc/hosts
        - vulnerable to DNS-over-HTTPS
    - macOS: pf firewall
    - Windows: Windows firewall via Powershell
- How do you hard-block apps?
    - macOS: daemon via launchd + NSWorkspaceWillLaunchApplicationNotification
        - PyObjC package will allow hooking into this
    - Windows: daemon via Windows Services through Powershell + repeatedly checking to kill
- How do you make the config un-modifiable, during blocks or otherwise?
    - check for running blocks before making changes
    - have daemon set file watcher + store copy of the config in memory as variable
    - overwrite config file as necessary
- How do you soft-block websites?
    - block same way as hard-blocked sites initially
    - get daemon to poll `netstat` every second and prompt GUI popup if detected
    - if user chooses to continue, unblock that specific site + set 15 min timer before blocking again
- How do you soft-block apps?
    - same way as hard-blocked apps initially
    - if detected, prompt GUI popup
    - if user chooses to continue, unblock that specific app + set 15 min timer before blocking again

### Daemon Logistics
- How do you recover the daemon if killed/make the daemon un-killable?
    - have a monitor process to revive the daemon process if it detects that the process is no longer running
- How do you run a Python program as a daemon/build a daemon in Python?
    - macOS: launchctl/launchd + plist
    - Windows: Windows services via Powershell

### Packaging
- How are we packaging up the app?
    - PyInstaller, run on each platform
    - Possibly set up CI for this

### Technologies
- Python (stdlib not included)
    - PySide/QT (GUI)
    - PyObjC (monitoring for app launches, macOS)
    - PyInstaller (packaging + binaries)
- System
    - pf firewall (blocking IPs, macOS)
    - Windows Firewall via Powershell (blocking IPs, Windows)
    - launchd (running as background process, macOS)
    - Windows services via Powershell (running as background process, Windows)

## Superseding these Apps/Extensions
- [SelfControl](http://selfcontrolapp.com)
- [Serene](https://sereneapp.com/#1581441799784-6afc0abc-409e)
    - macOS only
    - requires extension for blocking sites
    - advanced notification functionality not available
- [Monofocus](https://monofocus.app)
    - macOS only
    - shows popup/menu bar item of current task only, does not block
- [HazeOver: Distraction Dimmer™ for Productivity on Mac](https://hazeover.com)
    - macOS only
    - dims windows, does not do anything else
- [Freedom - Block Websites, Apps, and the Internet](https://freedom.to)
    - paid (subscription or $129 for life)
    - cannot run soft blocking and hard blocking simultaneously
    - advanced notification functionality not available
- [StayFocusd - Chrome Web Store](https://chrome.google.com/webstore/detail/stayfocusd/laankejkbhbdhmipfmgcngdelahlfoji)
    - Chromium only
    - does not block apps
- [LeechBlock NG – Get this Extension for 🦊 Firefox (en-US)](https://addons.mozilla.org/en-US/firefox/addon/leechblock-ng/)
    - Firefox only
    - does not block apps
- [BlockSite: Easily block distracting websites and apps](https://blocksite.co)
    - Desktop app is Windows only
    - Extensions uses Google Analytics, user data is shared with third-parties

## Links
[Moved these to my Raindrop.io collection.](https://raindrop.io/ThatNerd/lento-21974083)
