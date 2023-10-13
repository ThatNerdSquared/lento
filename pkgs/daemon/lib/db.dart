import 'dart:io';
import 'package:collection/collection.dart';
import 'package:logging/logging.dart';
import 'package:meta/meta.dart';
import 'package:sqlite3/sqlite3.dart';
import 'config.dart';
import 'notifs.dart';

// i tried to make these extension methods, but for some reason
// it didn't work and idk why so they're just funcs for now
bool toBool(int x) => x == 1;
// ignore: avoid_positional_boolean_parameters
int toInt(bool x) => (x ? 1 : 0);

bool initialized = false;
final log = Logger('File: db.dart');
String dbPath = '';

@immutable
class BlockedAppItem {
  final String name;
  final bool isRestrictedAccess;
  final String? popupMessage;
  final DateTime? lastChallenged;
  final bool canBypassRestriction;

  BlockedAppItem({
    required this.name,
    required this.isRestrictedAccess,
    required this.popupMessage,
    required this.lastChallenged,
    required this.canBypassRestriction,
  });
}

@immutable
class BlockedWebsiteItem {
  final Uri url;
  final bool isRestrictedAccess;
  final String? popupMessage;
  final DateTime? lastChallenged;
  final bool canBypassRestriction;

  BlockedWebsiteItem({
    required this.url,
    required this.isRestrictedAccess,
    required this.popupMessage,
    required this.lastChallenged,
    required this.canBypassRestriction,
  });

  /// Used to avoid showing popups repeatedly, which happens when
  /// a blocked site sends multiple requests from loading assets, etc
  bool wasRecentlyChallenged() {
    return lastChallenged != null &&
        DateTime.now().difference(lastChallenged!).inSeconds < 3;
  }

  void setChallenged() {
    // lastChallenged = DateTime.now();
  }
}

void init({required String path}) {
  dbPath = path;
  final db = sqlite3.open(dbPath);
  db.execute('''
    PRAGMA user_version = 1;

    CREATE TABLE $blockedAppsTable(
      name varchar(100),
      isRestrictedAccess int,
      popupMessage varchar(100),
      lastChallenged varchar(50),
      canBypassRestriction int
    );

    CREATE TABLE $blockedSitesTable(
      url varchar(200),
      isRestrictedAccess int,
      popupMessage varchar(100),
      lastChallenged varchar(50),
      canBypassRestriction int
    );

    CREATE TABLE $bannerQueueTable(
      queueNum int,
      title varchar(100),
      message varchar(100),
      triggerTime varchar(50)
    );

    CREATE TABLE timer(
      end_time varchar(50)
    );

  ''');
  log.info('DB initialized.');
  db.dispose();
}

bool mainTimerLoopExists() {
  if (!File(defaultDBFilePath).existsSync()) {
    return false;
  }
  final db = sqlite3.open(dbPath);
  final exists = db.select('SELECT * FROM timer').isEmpty;
  db.dispose();
  return !exists;
}

void saveAppData(Map apps) {
  final db = sqlite3.open(dbPath);
  final appInsertCmds = [];

  for (final name in apps.keys) {
    final isRestrictedAccess = toInt(apps[name]['isRestrictedAccess']);
    final popupMessage = apps[name]['popupMessage'];
    final lastChallenged = apps[name]['lastChallenged'];
    final canBypassRestriction = apps[name]['canBypassRestriction'] ?? 0;

    appInsertCmds.add(
      '''INSERT INTO $blockedAppsTable (name, isRestrictedAccess, popupMessage, lastChallenged, canBypassRestriction)
        VALUES ("$name", $isRestrictedAccess, "$popupMessage", "$lastChallenged", $canBypassRestriction);''',
    );
  }

  /// always use double quotes when inserting strings to db via sqlite,
  /// as double quotes allows a string like "O'Hara" to be inserting without
  /// interfering with the quotes of the string (as opposed to 'O'Hara')

  db.execute('''
  BEGIN TRANSACTION;
  ${appInsertCmds.join('\n')}
  COMMIT;
  ''');
  db.dispose();
}

void saveWebsiteData(Map websites) {
  final db = sqlite3.open(dbPath);
  final siteInsertCmds = [];
  for (String url in websites.keys) {
    final isRestrictedAccess = toInt(websites[url]['isRestrictedAccess']);
    final popupMessage = websites[url]['popupMessage'];
    final lastChallenged = websites[url]['lastChallenged'];
    final canBypassRestriction = websites[url]['canBypassRestriction'] ?? 0;

    siteInsertCmds.add(
      '''INSERT INTO $blockedSitesTable (url, isRestrictedAccess, popupMessage, lastChallenged, canBypassRestriction)
        VALUES ("$url", $isRestrictedAccess, "$popupMessage", "$lastChallenged", $canBypassRestriction);''',
    );
  }

  db.execute('''
  BEGIN TRANSACTION;
  ${siteInsertCmds.join('\n')}
  COMMIT;
  ''');

  db.dispose();
}

void saveBannerData(List bannerText, List bannerTriggerTimes) {
  final db = sqlite3.open(dbPath);
  var bannerData = '';
  for (var pair in IterableZip([bannerText, bannerTriggerTimes])) {
    log.info(pair.elementAt(0));
    String bannerTitle = pair.elementAt(0).keys.elementAt(0);
    String bannerMessage = pair.elementAt(0)[bannerTitle];
    var bannerTriggerTime = pair.elementAt(1).toString();

    bannerData +=
        '''INSERT INTO banner (banner_title, banner_message, trigger_time)
        VALUES ("$bannerTitle", "$bannerMessage", "$bannerTriggerTime");\n''';
  }

  db.execute('''
  BEGIN TRANSACTION;
  $bannerData
  COMMIT;
  ''');

  db.dispose();
}

void saveEndTime(DateTime endTime) {
  final db = sqlite3.open(dbPath);
  final endTimeString = endTime.toString();
  db.execute('''
  INSERT INTO timer (end_time)
  VALUES ("$endTimeString");
  ''');

  db.dispose();
}

Map buildAppInfo() {
  final db = sqlite3.open(dbPath);
  var apps = {}; // add apps to cardInfo from db
  List dbAppBlockInfo = db.select('''
  SELECT * FROM app_blocks
  ''');

  for (var appInfo in dbAppBlockInfo) {
    String procName = appInfo['proc_name'];
    int isSoftBlockInt = appInfo['is_soft_block'];
    var isSoftBlock = isSoftBlockInt == 1 ? true : false;
    int isAllowedInt = appInfo['is_allowed'];
    var isAllowed = isAllowedInt == 1 ? true : false;
    String popupMessage = appInfo['popup_msg'];
    var lastOpened = DateTime.parse(appInfo['last_opened']);

    apps[procName] = {
      'isSoftBlock': isSoftBlock,
      'isAllowed': isAllowed,
      'popupMessage': popupMessage,
      'lastOpened': lastOpened
    };
  }

  db.dispose();
  return apps;
}

Map buildWebsiteInfo() {
  final db = sqlite3.open(dbPath);
  var websites = {}; // add websites to cardInfo from db
  List dbWebsiteBlockInfo = db.select('''
  SELECT * FROM website_blocks
  ''');

  for (var websiteInfo in dbWebsiteBlockInfo) {
    String url = websiteInfo['url'];
    int isSoftBlockInt = websiteInfo['is_soft_block'];
    var isSoftBlock = isSoftBlockInt == 1 ? true : false;
    int isAllowedInt = websiteInfo['is_allowed'];
    var isAllowed = isAllowedInt == 1 ? true : false;
    String popupMessage = websiteInfo['popup_msg'];

    websites[url] = {
      'isSoftBlock': isSoftBlock,
      'isAllowed': isAllowed,
      'popupMessage': popupMessage
    };
  }

  db.dispose();
  return websites;
}

List buildBannerInfo() {
  final db = sqlite3.open(dbPath);
  var bannerText = [];
  var bannerTriggerTimes = [];

  List dbBannerInfo = db.select('''
  SELECT * FROM banner
  ''');

  for (var bannerInfo in dbBannerInfo) {
    bannerText.add({bannerInfo['banner_title']: bannerInfo['banner_message']});
    bannerTriggerTimes.add(DateTime.parse(bannerInfo['trigger_time']));
  }

  db.dispose();
  return [bannerText, bannerTriggerTimes];
}

DateTime getEndTime() {
  final db = sqlite3.open(dbPath);
  final dbTimeInfo = db.select('''
  SELECT * FROM timer
  ''');

  db.dispose();
  return DateTime.parse(dbTimeInfo[0]['end_time']);
}

void reset() {
  final db = File(dbPath);
  db.deleteSync();
}

void saveBannerQueue(List<BannerNotif> bannerQueue) {
  final db = sqlite3.open(dbPath);
  final cmd = [
    'INSERT INTO $bannerQueueTable (queueNum, title, message, triggerTime) VALUES'
  ];
  var queueNum = 1;
  for (final banner in bannerQueue) {
    final terminator = queueNum == bannerQueue.length ? ';' : ',';
    cmd.add(
        '($queueNum, "${banner.title}", "${banner.message}", "${banner.triggerTime.toIso8601String()}")$terminator');
    queueNum += 1;
  }
  db.execute(cmd.join('\n'));
  db.dispose();
}

List<BannerNotif> getBannerQueue() {
  final db = sqlite3.open(dbPath);
  final rawBanners = db.select('SELECT * FROM $bannerQueueTable');
  db.dispose();
  return rawBanners
      .map((rb) => BannerNotif(
          title: rb['title'],
          message: rb['message'],
          triggerTime: DateTime.parse(rb['triggerTime'])))
      .toList();
}

void popBannerOffQueue() {
  final db = sqlite3.open(dbPath);
  db.execute('''
  DELETE FROM $bannerQueueTable WHERE queueNum = (SELECT min(queueNum) FROM $bannerQueueTable);
  ''');
  log.info('Top banner popped off queue.');
  db.dispose();
}

bool isNotBlockedApp(String appName) {
  final db = sqlite3.open(dbPath);
  final blockedAppNames = db.select('SELECT name FROM $blockedAppsTable');
  db.dispose();
  return !blockedAppNames.rows.any((e) => e[0] == appName);
}

BlockedAppItem getBlockedApp(String appName) {
  final db = sqlite3.open(dbPath);
  final blockedApp = db.select(
    'SELECT * FROM $blockedAppsTable WHERE name = "$appName"',
  )[0];
  db.dispose();
  return BlockedAppItem(
    name: blockedApp['name'],
    isRestrictedAccess: toBool(blockedApp['isRestrictedAccess']),
    popupMessage: blockedApp['popupMessage'],
    lastChallenged: blockedApp['lastChallenged'] == 'null'
        ? null
        : DateTime.parse(blockedApp['lastChallenged']),
    canBypassRestriction: toBool(blockedApp['canBypassRestriction']),
  );
}

void recordAppChallenge(BlockedAppItem app) {
  final db = sqlite3.open(dbPath);
  db.execute(
    'UPDATE $blockedAppsTable SET lastChallenged = "${DateTime.now()}" WHERE name = "${app.name}"',
  );
  db.dispose();
}

void setAppRestrictionBypass({
  required BlockedAppItem app,
  required bool canBypassRestriction,
}) {
  final db = sqlite3.open(dbPath);
  db.execute(
    'UPDATE $blockedAppsTable SET canBypassRestriction = ${toInt(canBypassRestriction)} WHERE name = "${app.name}"',
  );
  db.dispose();
}

Uri? detectBlockedSite(String rawURL) {
  final db = sqlite3.open(dbPath);
  final blockedSiteURLs = db.select('SELECT url FROM $blockedSitesTable');
  db.dispose();
  for (final row in blockedSiteURLs.rows) {
    if (rawURL.contains(row.first.toString())) {
      return Uri(host: row.first.toString());
    }
  }
  return null;
}

BlockedWebsiteItem getBlockedSite(Uri siteURL) {
  final db = sqlite3.open(dbPath);
  final blockedSite = db.select(
    'SELECT * FROM $blockedSitesTable WHERE url = "${siteURL.host}"',
  )[0];
  db.dispose();
  return BlockedWebsiteItem(
    url: siteURL,
    isRestrictedAccess: toBool(blockedSite['isRestrictedAccess']),
    popupMessage: blockedSite['popupMessage'],
    lastChallenged: blockedSite['lastChallenged'] == 'null'
        ? null
        : DateTime.parse(blockedSite['lastChallenged']),
    canBypassRestriction: toBool(blockedSite['canBypassRestriction']),
  );
}

void recordSiteChallenge(BlockedWebsiteItem site) {
  final db = sqlite3.open(dbPath);
  db.execute(
    'UPDATE $blockedSitesTable SET lastChallenged = "${DateTime.now()}" WHERE url = "${site.url.toString()}"',
  );
  db.dispose();
}

void setSiteRestrictionBypass({
  required BlockedWebsiteItem site,
  required bool canBypassRestriction,
}) {
  final db = sqlite3.open(dbPath);
  db.execute(
    'UPDATE $blockedSitesTable SET canBypassRestriction = ${toInt(canBypassRestriction)} WHERE url = "${site.url.toString()}"',
  );
  db.dispose();
}
