# `LentoDaemon` Documentation

## Proxy flow
*Note: the below diagram should render as a flowchart when previewed (Cmd/Ctrl-Shift-V in VSCode). Ensure your Markdown preview has Mermaid support - you may need [this VSCode extension](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid), [this neovim extension](https://github.com/iamcco/markdown-preview.nvim), or equivalent.*
```mermaid
flowchart TD

classDef default fill:#88a2bc
classDef action fill:#f0dbb0
classDef result fill:#d99477

n1(User accesses site)
n2(Is site blocked?)
n3(Is site restricted access?)
n4(Was site recently challenged?)
n4.5(Was site recently challenged?)
n5(Is the site allowed to bypass restrictions?)
n6("`Was the site challenged less than *restrictionBypassTTL* minutes ago?`")
n7(Approved by user?)

a1(Show hard blocked popup):::action
a2(Record challenge):::action
a2.1(Record challenge):::action
a2.2(Record challenge):::action
a3(Challenge restricted access):::action
a4(Show restricted access popup):::action
a5(Give site restriction bypass in DB):::action

r1(Forward connection):::result
r1.1(Forward connection):::result
r1.2(Forward connection):::result
r2(Reject connection):::result
r2.5(Reject connection):::result

n1 --> n2
n2 -->|no|r1
n2 -->|yes|n3
n3 -->|no|n4
n4 -->|no|a1
a1 --> a2
a2 --> r2
n4 -->|yes|r2
n3 -->|yes|n5
n5 -->|yes|n6
n6 -->|yes|r1.1
n5 -->|no|a3
n6 -->|no|a3

a3 --> n4.5
n4.5 -->|yes|a2.1
n4.5 -->|no|a4
a2.1 --> r2.5
a4 --> n7
n7 -->|no|a2.1
n7 -->|yes|a2.2
a2.2 --> a5
a5 --> r1.2
```


## Debugging

### Sending test data to the daemon
The `docs/example-daemon-input.json` file is the canonical spec for the data input format expected by the daemon. All data sent to and requested by the daemon should match this file - if not, either it should be corrected, or the `example-daemon-input.json` file updated to match.

A script is included to send this data to the daemon for manual debugging (the daemon should output a "DaemonServer on port XXXXX" log message that you can retrieve the port number from).
```
dart run :liveammotest [port]
```

### Manual testing
If you're running in dev, you want to use the `--devmode` flag when running the daemon so that it can find the `notifhelper` build in the repo, as opposed to a bundled version of it in prod:
```
dart run daemon --devmode
```
For VSCode users, this is included in the `launch.json` - just select the `daemon (dev mode)` configuration.

### DB
To inspect the state of the DB at runtime, I would recommend opening it up in some sort of SQLite DB browser. I use [DB Browser for SQLite](https://sqlitebrowser.org/) (download at link, or below for macOS):
```bash
brew install db-browser-for-sqlite
```

## Tests
To run the tests, you will first need to generate the appropriate mocks:
```bash
dart run build_runner build
```

- There is a very minimal test suite for the daemon - not everything is covered (most notably, none of the proxy)
- We have a mix of unit tests and integration tests
- While these get run in CI, please make regular local runs when extending/refactoring the daemon to avoid breaking functionality
- I would like to expand the test suite to cover more "user paths", so mainly integration tests that cover different possible situations encountered by the proxy/appblocker
    - Avoid adding more unit tests, the usefulness-to-maintenance-required ratio isn't great, and would likely require extensive mocking (db, `Process.run`s, etc)