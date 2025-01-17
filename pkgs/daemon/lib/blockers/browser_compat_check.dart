/// Firefox doesn't use SOCKS5 by default when using the system default
/// proxy - it defaults to SOCKS4. Since our proxy only supports SOCKS5,
/// [ensureFirefoxCompat] is required in order to inject a setting into
/// the `user.js` config file to switch the default SOCKS version to 5.
/// Hopefully at some point in the future this will become redundant -
/// maybe we should file an issue with FF about it?

import 'dart:io';

import 'package:meta/meta.dart';
import 'package:path/path.dart' as p;

void ensureFirefoxCompat() {
  final profilesDir = _getFirefoxProfilesDir();
  for (final dir in profilesDir.listSync().whereType<Directory>()) {
    final userJsFile = File(p.join(dir.path, 'user.js'));
    if (!userJsFile.existsSync()) {
      userJsFile.createSync();
    }
    final userJsText = userJsFile.readAsLinesSync();
    userJsFile.writeAsStringSync(addPayloadToUserJS(userJsText));
  }
}

@visibleForTesting
String addPayloadToUserJS(List<String> userJS) {
  final lentoConfigPayload = [
    '// DO NOT REMOVE - AUTOMATICALLY ADDED BY LENTO TO ENSURE BLOCK COMPATABILITY',
    'user_pref("network.proxy.default_pac_script_socks_version", 5);',
  ];
  return Set.of(userJS).containsAll(lentoConfigPayload)
      ? userJS.join('\n')
      : (userJS + lentoConfigPayload).join('\n');
}

Directory _getFirefoxProfilesDir() {
  final envVars = Platform.environment;
  switch (Platform.operatingSystem) {
    case 'macos':
      return Directory(p.join(envVars['HOME']!, 'Library',
          'Application Support', 'Firefox', 'Profiles'));
    case 'windows':
      return Directory(p.join(
          envVars[
              'APPDATA']!, // does this work? i know UserProfile returns the home dir
          'Mozilla',
          'Firefox',
          'Profiles'));
    default:
      throw UnimplementedError(
          'getFirefoxProfilesDir does not support ${Platform.operatingSystem} yet!');
  }
}
