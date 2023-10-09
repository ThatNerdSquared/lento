import 'dart:io';

PlatformProxySettings getPlatformProxySettings() =>
    switch (Platform.operatingSystem) {
      'macos' => MacosProxySettings(),
      _ => throw UnimplementedError(
          'Platform proxy settings for ${Platform.operatingSystem} not yet supported!',
        )
    };

abstract class PlatformProxySettings {
  void enableProxy(int proxyPort);

  void disableProxy();
}

class MacosProxySettings extends PlatformProxySettings {
  @override
  void enableProxy(int proxyPort) {
    Process.runSync(
      'networksetup',
      ['-setsocksfirewallproxy', 'wi-fi', 'localhost', proxyPort.toString()],
    );
  }

  @override
  void disableProxy() {
    Process.runSync(
      'networksetup',
      ['-setsocksfirewallproxystate', 'wi-fi', 'off'],
    );
  }
}
