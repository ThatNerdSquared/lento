import 'dart:io';
import 'package:collection/collection.dart';
import 'package:logging/logging.dart';
import 'package:sqlite3/sqlite3.dart';
import 'config.dart';

/// Below is a summary of the information cardInfo stores.

/// cardInfo {
/// apps : {procName : {isSoftBlock: <bool>, isAllowed: <bool>, popupMessage: <String>, lastOpened: <DateTime>}},
/// websites : {url: {isSoftBlock: <bool>, isAllowed: <bool>, popupMessage: <String>, lastOpened: <DateTime>}},
/// bannerText : [{bannerTitle: bannerMessage}],
/// blockDuration : <int>,
/// bannerTriggerTimes : [<int>],
/// }

bool initialized = false;
final log = Logger('File: db.dart');

Future<bool> checkForDB() async {
  final dbFile = File(dbFilePath);
  final doesFileExist = await dbFile.exists();
  if (doesFileExist) {
    final db = sqlite3.open(dbFilePath);
    final timeExists = db.select('SELECT * FROM timer').isEmpty ? false : true;
    db.dispose();
    return timeExists;
  } else {
    return false;
  }
}

void init() {
  final db = sqlite3.open(dbFilePath);
  db.execute('''
    PRAGMA user_version = 1;

    CREATE TABLE app_blocks(
      proc_name varchar(100),
      is_soft_block int,
      is_allowed int,
      popup_msg varchar(200),
      last_opened varchar(50)
    );

    CREATE TABLE website_blocks(
      url varchar(200),
      is_soft_block int,
      is_allowed int, 
      popup_msg varchar(200),
      last_opened varchar(50)
    );

    CREATE TABLE banner(
      banner_title varchar(100),
      banner_message varchar(100),
      trigger_time varchar(50)
    );

    CREATE TABLE timer(
      end_time varchar(50)
    );

  ''');

  db.dispose();
}

Future<bool> mainTimerLoopExists() async {
  if (await File(dbFilePath).exists()) {
    final db = sqlite3.open(dbFilePath);
    final exists = db.select('SELECT * FROM timer').isEmpty ? false : true;

    db.dispose();
    return exists;
  } else {
    init();
    print('made db');
    return false;
  }
}

void saveAppData(Map apps) {
  final db = sqlite3.open(dbFilePath);
  var appData = '';
  for (String procName in apps.keys) {
    // save app data to db
    // log.info("*********");
    // log.info(procName.toString());
    bool isSoftBlock = apps[procName]['isSoftBlock'];
    // log.info(isSoftBlock.toString());
    var isSoftBlockInt = isSoftBlock ? 1 : 0;
    // log.info(isSoftBlockInt.toString());
    bool isAllowed = apps[procName]['isAllowed'];
    // log.info(isAllowed.toString());
    var isAllowedInt = isAllowed ? 1 : 0;
    // log.info(isAllowedInt.toString());
    String popupMessage = apps[procName]['popupMessage'];
    // log.info(popupMessage.toString());
    var lastOpened = apps[procName]['lastOpened'].toString();
    // log.info(lastOpened.toString());

    appData +=
        '''INSERT INTO app_blocks (proc_name, is_soft_block, is_allowed, popup_msg, last_opened)
        VALUES ("$procName", $isSoftBlockInt, $isAllowedInt, "$popupMessage", "$lastOpened");\n''';
  }

  /// always use double quotes when inserting strings to db via sqlite,
  /// as double quotes allows a string like "O'Hara" to be inserting without
  /// interfering with the quotes of the string (as opposed to 'O'Hara')

  db.execute('''
  BEGIN TRANSACTION;
  $appData
  COMMIT;
  ''');
  db.dispose();
}

void saveWebsiteData(Map websites) {
  final db = sqlite3.open(dbFilePath);
  var websiteData = '';
  for (String url in websites.keys) {
    // save app data to db
    bool isSoftBlock = websites[url]['isSoftBlock'];
    var isSoftBlockInt = isSoftBlock ? 1 : 0;
    bool isAllowed = websites[url]['isAllowed'];
    var isAllowedInt = isAllowed ? 1 : 0;
    String popupMessage = websites[url]['popupMessage'];
    var lastOpened = websites[url]['lastAsked'].toString();

    websiteData +=
        '''INSERT INTO website_blocks (url, is_soft_block, is_allowed, popup_msg, last_opened)
        VALUES ("$url", $isSoftBlockInt, $isAllowedInt, "$popupMessage", "$lastOpened");\n''';
  }

  db.execute('''
  BEGIN TRANSACTION;
  $websiteData
  COMMIT;
  ''');

  db.dispose();
}

void saveBannerData(List bannerText, List bannerTriggerTimes) {
  final db = sqlite3.open(dbFilePath);
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

void saveTime(DateTime endTime) {
  final db = sqlite3.open(dbFilePath);
  final endTimeString = endTime.toString();
  db.execute('''
  INSERT INTO timer (end_time)
  VALUES ("$endTimeString");
  ''');

  db.dispose();
}

Map buildAppInfo() {
  final db = sqlite3.open(dbFilePath);
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
  final db = sqlite3.open(dbFilePath);
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
  final db = sqlite3.open(dbFilePath);
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

DateTime buildTimeInfo() {
  final db = sqlite3.open(dbFilePath);
  List dbTimeInfo = db.select('''
  SELECT * FROM timer
  ''');

  db.dispose();
  return DateTime.parse(dbTimeInfo[0]['end_time']);
}

void reset() {
  final db = File(dbFilePath);
  db.deleteSync();
}
