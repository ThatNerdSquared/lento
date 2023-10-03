import 'dart:io';

import 'package:path/path.dart' as p;

void ensureFirefoxCompat() {
  final lentoConfigPayload = [
    '// DO NOT REMOVE - AUTOMATICALLY ADDED BY LENTO TO ENSURE BLOCK COMPATABILITY',
    'user_pref("network.proxy.default_pac_script_socks_version", 5);',
  ];
  final profilesDir = getFirefoxProfilesDir();
  for (final dir in profilesDir.listSync().whereType<Directory>()) {
    final userJsFile = File(p.join(dir.path, 'user.js'));
    if (!userJsFile.existsSync()) {
      userJsFile.createSync();
      return userJsFile.writeAsStringSync(lentoConfigPayload.join('\n'));
    }
    var userJsText = userJsFile.readAsLinesSync();
    if (!Set.of(userJsText).containsAll(lentoConfigPayload)) {
      userJsFile.writeAsStringSync(
        (userJsText + lentoConfigPayload).join('\n'),
      );
    }
  }
}

Directory getFirefoxProfilesDir() {
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
