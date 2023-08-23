import 'dart:io';
import 'package:collection/collection.dart';
import 'package:logging/logging.dart';
import 'package:sqlite3/sqlite3.dart';
import 'config.dart';

/// Below is a summary of the information cardInfo stores.

/// cardInfo {
/// apps : {procName : {isSoftBlock: <bool>, lastOpened: <DateTime>, isAllowed: <bool>, popupMsg: <String>}},
/// websites : {url: {isSoftBlock: <bool>, lastOpened: <DateTime>, isAllowed: <bool>, popupMsg: <String>}},
/// bannerText : [{bannerTitle: bannerMessage}],
/// blockDuration : <int>,
/// bannerTriggerTimes : [<int>],
/// }

bool initialized = false;
final log = Logger('File: DB');

Future<void> checkForDB() async {
  final db = File(dbFilePath);
  final doesFileExist = await db.exists();
  if (!doesFileExist) {
    db.create();
  }
}

void init() {
  if (!initialized) {
    checkForDB();
    final db = sqlite3.open(dbFilePath);
    db.execute('''
      PRAGMA user_version = 1;

      CREATE TABLE app_blocks(
        proc_name varchar(100),
        is_soft_block int,
        last_opened varchar(50),
        is_allowed int,
        popup_msg varchar(100)
      );

      CREATE TABLE website_blocks(
        url varchar(200),
        is_soft_block int,
        last_opened varchar(50),
        is_allowed int, 
        popup_msg varchar(100)
      );

      CREATE TABLE banner(
        banner_title varchar(100),
        banner_message varchar(100),
        trigger_time varchar(50)
      );

      CREATE TABLE time(
        end_time varchar(50)
      );

    ''');

    db.dispose();
    initialized = true;
  }
}

bool mainTimerLoopExists() {
  final db = sqlite3.open(dbFilePath);
  final exists =
      db.select('SELECT count(*) FROM MainTimerLoop').isEmpty ? true : false;

  return exists;
}

void saveAppData(Map apps) {
  final db = sqlite3.open(dbFilePath);
  var appData = '';
  for (var key in apps.keys) {
    // save app data to db
    var procName = key;
    var isSoftBlock = apps[key][0];
    var isSoftBlockInt = isSoftBlock ? 1 : 0;
    var lastOpened = apps[key][1];
    var isAllowed = apps[key][2];
    var isAllowedInt = isAllowed ? 1 : 0;
    var popupMessage = apps[key][3];

    appData +=
        'INSERT INTO app_blocks (proc_name, is_soft_block, last_opened, is_allowed, popup_msg) table VALUES ($procName, $isSoftBlockInt, $lastOpened, $isAllowedInt, $popupMessage);\n';
  }

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
  for (var key in websites.keys) {
    // save app data to db
    var url = key;
    var isSoftBlock = websites[key][0];
    var isSoftBlockInt = isSoftBlock ? 1 : 0;
    var lastOpened = websites[key][1];
    var isAllowed = websites[key][2];
    var isAllowedInt = isAllowed ? 1 : 0;
    var popupMessage = websites[key][3];

    websiteData +=
        'INSERT INTO website_blocks (url, is_soft_block, last_opened, is_allowed, popup_msg) table VALUES ($url, $isSoftBlockInt, $lastOpened, $isAllowedInt, $popupMessage);\n';
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
    String bannerTitle = pair[0].keys().elementAt(0);
    String bannerMessage = pair[0][bannerTitle];
    var bannerTriggerTime = bannerTriggerTimes[0].toString();

    bannerData +=
        'INSERT INTO banner (banner_title, banner_message, trigger_time) table VALUES ($bannerTitle, $bannerMessage, $bannerTriggerTime);\n';
  }

  db.execute('''
  BEGIN TRANSACTION
  $bannerData
  COMMIT;
  ''');

  db.dispose();
}

void saveTime(DateTime endTime) {
  final db = sqlite3.open(dbFilePath);
  final endTimeString = endTime.toString();
  db.execute('''
  INSERT INTO time (start_time, end_time)
  VALUES ($endTimeString)
  ''');

  db.dispose();
}

Map buildCardInfo() {
  final db = sqlite3.open(dbFilePath);
  var cardInfo = {};

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

    apps[procName] = [isSoftBlock, isAllowed, popupMessage];
  }

  cardInfo['apps'] = apps;

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

    websites[url] = [isSoftBlock, isAllowed, popupMessage];
  }

  cardInfo['websites'] = websites;

  var bannerText = [];
  var bannerTriggerTimes = [];

  List dbBannerInfo = db.select('''
  SELECT * FROM banner
  ''');

  for (var bannerInfo in dbBannerInfo) {
    bannerText.add({bannerInfo['banner_title']: bannerInfo['banner_message']});
    bannerTriggerTimes.add(DateTime.parse(bannerInfo['trigger_time']));
  }

  cardInfo['bannerTitleMessage'] = bannerText;
  cardInfo['banner_trigger_times'] = bannerTriggerTimes;

  List dbTimeInfo = db.select('''
  SELECT * FROM time
  ''');

  cardInfo['endTime'] = DateTime.parse(dbTimeInfo[0]['end_time']);

  db.dispose();
  return cardInfo;
}

void clear() {
  final db = sqlite3.open(dbFilePath);
  db.execute('''
  DELETE FROM app_blocks;
  DELETE FROM website_blocks;
  DELETE FROM banner;
  DELETE FROM time;
  ''');
}
