/// THIS IS A VERY ROUGH DRAFT, PRIMARLY FOR TESTING.
/// THERE ARE NUMEROUS PROBLEMS IN THIS FILE, INCLUDING BUT NOT LIMITED TO:
/// - manual reads from the `lentosettings.json` file - all JSON handling should
///   be handled by a method on the [JsonBackend] class
/// - idk if a while loop + sleep is the best way to wait for daemon to write its
///   port to the settings file
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
import 'package:path/path.dart' as p;

import 'backend/card_data.dart';
import 'backend/json_backend.dart';
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

  Map createDaemonInput(LentoCardData card) {
    return {
      'blockDuration': card.blockDuration,
      'apps': card.blockedApps.map((key, value) => MapEntry(value.appName, {
            'isRestrictedAccess': value.isRestrictedAccess,
            'popupMessage': value.customPopupId
          })),
      'websites': card.blockedSites
          .map((key, value) => MapEntry(value.siteUrl.toString(), {
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
}
