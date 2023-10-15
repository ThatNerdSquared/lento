import 'dart:io';

const defaultDBFilePath = 'lentoDB.sqlite3';
const lentoSettingsPath = 'lentosettings.json';
const macOSNotifHelperPath =
    'LentoNotifHelper.app/Contents/MacOS/LentoNotifHelper';

String devNotifHelperPath() => switch (Platform.operatingSystem) {
      'macos' =>
        '../notif_helper/build/macos/Build/Products/Release/LentoNotifHelper.app/Contents/MacOS/LentoNotifHelper',
      _ => throw Exception(
          'devNotifHelperPath not yet implemented for ${Platform.operatingSystem}!'),
    };

int proxyPort = 0;
int restrictionBypassTTL = 15;

const bannerQueueTable = 'bannerQueue';
const blockedAppsTable = 'blockedApps';
const blockedSitesTable = 'blockedSites';
