# lento notifs spec

## concept

### types

- popups
  - fire when blocked item is accessed
  - customization: message ONLY, set PER BLOCKITEM
    - custom message specified in block item editor
  - **softblock (restricted access) popup**
    - "Allow" and "Cancel" options, "Cancel" is DEFAULT
  - **hardblock popup**
    - singular "OK" option as DEFAULT
- banners
  - fire at different time points during the block, as set by user PER CARD
  - can be set to fire at any point in the block
    - slider allows setting at 5-minute increments (can be set at 5m, 10m, etc)
  - two banners CANNOT fire at the same time
  - customization: title, message set PER BANNER
    - banners are shown in the "Scheduled Events" togglelist for each card
    - each card can have different banners enabled/disabled
    - editing happens in banner editor (title, message, time points on slider, test)
    - in future, could allow selection from provided set of sound effects

## implementation

- flutter crossplatform app?
  - flutter exes do not exist[^1] and flutter cannot be used from a pure dart executable
  - **possible problem: flutter app with invisible/no window => how to implement?**
    - use [bitsdojo_window](https://pub.dev/packages/bitsdojo_window) to hide window
  - need to create app package that opens, taking config from stdin, and then spits out the result to stdout
    - use `--dart-entrypoint-args` for passing in args in dev
    - args can be passed in normally as strings with the compiled executable
  - possible packages:
    - popups
      - `flutter_platform_alert` looks promising
    - banners
      - `flutter_local_notifications`: does not support windows, a [draft PR to add linux/windows support](https://github.com/MaikuB/flutter_local_notifications/pull/1473) has been going since 2022 and is currently stalled
      - `windows_notification`: only supports windows
      - combining these two packages
      - ~~`awesome_notifications`: does not support desktop platforms, [despite what it says in the pub.dev platform list](https://github.com/rafaelsetragni/awesome_notifications/issues/637)~~
      - ~~`local_notifier` looks promising~~

### past experiments

- macos
  - ~~shell out to applescript~~
    - popups
      - unable to set custom icon, or acceptable default icon (doesn't have weird folder icon, etc)
      - found possible solution using "tell application" but messy, prone to breakage
    - banner
      - unable to set custom icon, or acceptable default icon
  - ~~swift script~~
    - cannot steal focus in NSAlert, unable to use keyboard shortcuts to respond to alert even after interaction + setting `keyEquivalent`
    - unable to implement banner notifs without app bundle
      - `2023-08-08 17:15:20.390 swift-frontend[22141:231308] *** Terminating app due to uncaught exception 'NSInternalInconsistencyException', reason: 'bundleProxyForCurrentProcess is nil: mainBundle.bundleURL'`
  - swift app?
- windows
  - script with powershell?
    - ~~banners~~ (replaced by flutter)
      - https://github.com/GitHub30/toast-notification-examples/blob/main/README.md is extremely helpful
      - `ToastText02` works well, `ToastImageAndText02` might as well
      - note that at some point you have to define this `$AppId` variable - if you change it to any other AppId (which you can get a giant table of by running `Get-StartApps`) you can make the banner look like it came from that app
    - ~~popups~~
      - only been able to get ugly win32 version running so far: https://woshub.com/popup-notification-powershell/
      - example: `$wshell = New-Object -ComObject Wscript.Shell; $wshell.Popup("This item is blocked")`
      - some other solutions rely on importing and using some UWP libraries, but are very heavyweight
        - could implement later for prettier result
- linux
- ios (TBD)
- android (TBD)

[^1]: [Supported deployment platforms | Flutter](https://docs.flutter.dev/reference/supported-platforms#deploying-flutter)
