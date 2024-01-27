/// THIS IS A VERY ROUGH DRAFT, PRIMARLY FOR TESTING.
/// THERE ARE NUMEROUS PROBLEMS IN THIS FILE, INCLUDING BUT NOT LIMITED TO:
///
/// - manual reads from the `lentosettings.json` file - all JSON handling should
///   be handled by a method on the [JsonBackend] class
///
/// - idk if a while loop + sleep is the best way to wait for daemon to write its
///   port to the settings file
///
/// - [PlatformDaemonSettings.createDaemonInput] is EXTREMELY rough and does not
///   support things like banners yet. i think with time i want to standardize
///   the data formats such that we can just [LentoCardData.toJson] an entire
///   card and send it without having to manually convert to the daemon's
///   accepted format - but i'm doing this for now for testing purposes.
///
/// that being said, the general structure of [getPlatformDaemonSettings] with
/// the [PlatformDaemonSettings] abstract class and platform-specific subclasses
/// is fine. might need more methods on the abstract class but we can figure that
/// out later.

import 'dart:convert';
import 'dart:io';
import 'package:common/common.dart';
import 'package:flutter/services.dart';
import 'package:path/path.dart' as p;

import 'backend/card_data.dart';
import 'backend/json_backend.dart';
import 'config.dart';
import 'main.dart';

PlatformDaemonSettings getPlatformDaemonSettings() =>
    switch (Platform.operatingSystem) {
      'macos' => MacosDaemonSettings(),
      _ => throw UnimplementedError(
          'Platform daemon settings for ${Platform.operatingSystem} not yet supported!',
        )
    };

abstract class PlatformDaemonSettings {
  void sendBlockDataToDaemon(LentoCardData card);
  void launchDaemon();
  void isDaemonRunning();
  Map createDaemonInput(LentoCardData card) {
    return {
      'blockDuration': card.blockDuration,
      'apps': card.onlyApps.map((key, value) => MapEntry(value.itemName, {
            'isRestrictedAccess': value.isRestrictedAccess,
            'popupMessage': value.customPopupId
          })),
      'websites':
          card.onlyWebsites.map((key, value) => MapEntry(value.itemName, {
                'isRestrictedAccess': value.isRestrictedAccess,
                'popupMessage': value.customPopupId
              }))
    };
  }
}

class MacosDaemonSettings extends PlatformDaemonSettings {
  @override
  void sendBlockDataToDaemon(LentoCardData card) async {
    Process.run(p.join(platformAppSupportDir, 'lentodaemon').toString(), []);

    while (
        jsonDecode(JsonBackend().dataFile.readAsStringSync())['daemonPort'] ==
            null) {
      sleep(const Duration(seconds: 1));
    }
    final data = jsonDecode(JsonBackend().dataFile.readAsStringSync());
    final socket =
        await Socket.connect('localhost', int.parse(data['daemonPort']));
    socket.write(json.encode(createDaemonInput(card)));
  }

  @override
  void launchDaemon() async {
    var homeFolder = Config.homeFolder;
    dynamic lentoPlist;
    if (!File(
            '$homeFolder/Library/LaunchAgents/"ca.failsafe.lentodaemon.plist"')
        .existsSync()) {
      final lentoPlistString =
          await rootBundle.loadString('assets/ca.failsafe.lentodaemon.plist');
      lentoPlist = File(
          '$homeFolder/Library/LaunchAgents/"ca.failsafe.lentodaemon.plist"');
      lentoPlist.writeAsString(lentoPlistString);
    }
    Process.run('launchctl', ['load', lentoPlist]);
  }

  @override
  bool isDaemonRunning() {
    var processes = getPlatformProcessManager().rawProcesses();

    for (var process in processes) {
      if (process.contains('lentodaemon')) {
        return true;
      }
    }
    return false;
  }
}
