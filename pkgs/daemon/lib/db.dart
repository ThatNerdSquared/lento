import 'dart:io';
import 'package:collection/collection.dart';
import 'package:logging/logging.dart';
import 'package:sqlite3/sqlite3.dart';
import 'config.dart';

bool initialized = false;
final log = Logger('File: DB');

/// Below is a summary of the information cardInfo stores.
/// Keys with asterisks next to them denotes info that is only needed when a block starts for the first time.
/// Keys with tildas next to them denotes info that is needed only needed when a block restarts/info that is created as the daemon executes.
///
/// cardInfo {
/// <String> apps : {<String> proc_name : [<bool> is_soft_block, <bool> is_allowed, <String> popup_msg]},
/// <String> websites : {<String> url: [<bool> is_soft_block, <bool> is_allowed, <String> popup_msg]},
/// <String> banner_titles : [<String>]
/// <String> banner_messages : [<String>]
/// <String> banner_trigger_times : [<DateTime>]
/// *<String> block_duration : <int>,
/// *<String> banner_trigger_time_intervals : [<int>], (only used in daemon.dart, not needed in db)
/// ^<String> block_start_time : <DateTime>,
/// ^<String> block_end_time: <DateTime>
/// }

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
        is_allowed int,
        popup_msg varchar(100)
      );

      CREATE TABLE website_blocks(
        url varchar(200),
        is_soft_block int,
        is_allowed int, 
        popup_msg varchar(100)
      );

      CREATE TABLE banner(
        banner_title varchar(100),
        banner_message varchar(100),
        trigger_time varchar(50)
      );

      CREATE TABLE time(
        start_time varchar(50),
        end_time varchar(50)
      );

    ''');

    db.dispose();
    initialized = true;
  }
}


bool mainTimerLoopExists(){
  bool exists;
  final db = sqlite3.open(dbFilePath);

  if (db.select('SELECT count(*) FROM MainTimerLoop').isEmpty) {
    exists = false;
  } else {
    exists = true;
  }

  db.dispose();

  return exists;
}

void save(String table, dynamic row, dynamic data) {
  final db = sqlite3.open(dbFilePath);
  if (table == 'cardInfo') { // save cardInfo to db
    Map cardInfo = data;

    for (var key in cardInfo['apps'].keys) { // save app data to db
      var procName = key;
      var isSoftBlock = cardInfo['apps'][key][0];
      var isSoftBlockInt = isSoftBlock ? 0 : 1;
      var isAllowed = cardInfo['apps'][key][1];
      var isAllowedInt = isAllowed ? 0 : 1;
      var popupMessage = cardInfo['apps'][key][2];

      db.execute('''
      INSERT INTO app_blocks (proc_name, is_soft_block, is_allowed, popup_msg)
      VALUES ($procName, $isSoftBlockInt, $isAllowedInt, $popupMessage);
      ''');
    }

    for (var key in cardInfo['websites'].keys) { // save website data to db
      var url = key;
      var isSoftBlock = cardInfo['websites'][key][0];
      var isSoftBlockInt = isSoftBlock ? 0 : 1;
      var isAllowed = cardInfo['websites'][key][1];
      var isAllowedInt = isAllowed ? 0 : 1;
      var popupMessage = cardInfo['websites'][key][2];

      db.execute('''
      INSERT INTO website_blocks (proc_name, is_soft_block, is_allowed, popup_msg)
      VALUES ($url, $isSoftBlockInt, $isAllowedInt, $popupMessage);
      ''');
    }

    List bannerTitles = cardInfo['banner_titles'];
    List bannerMessages = cardInfo['banner_messages'];
    List bannerTriggerTimes = cardInfo['banner_trigger_times'];

    for (var pair in IterableZip<dynamic>([bannerTitles, bannerMessages, bannerTriggerTimes])) { 
      // save banner messages and banner trigger times to db
      String bannerTitle = pair[0];
      String bannerMessage = pair[1];
      var bannerTriggerTime = pair[2].toString();

      db.execute('''
      INSERT INTO banner (banner_title, banner_message, trigger_time)
      VALUES ($bannerTitle, $bannerMessage, $bannerTriggerTime);
      ''');
    }

    final startTime = cardInfo['block_start_time'];
    final endTime = cardInfo['block_end_time'];

    db.execute('''
    INSERT INTO time (start_time, end_time)
    VALUES ($startTime, $endTime)
    ''');

    db.dispose();

  } else { // save time to db
    var timeString = data.toString();

    db.execute('''
      INSERT INTO $table ($row)
      VALUES($timeString)
    ''');
  }
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
    var isSoftBlock =  isSoftBlockInt == 0 ? false : true;
    int isAllowedInt = appInfo['is_allowed'];
    var isAllowed = isAllowedInt == 0 ? false : true;
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
    var isSoftBlock =  isSoftBlockInt == 0 ? false : true;
    int isAllowedInt = websiteInfo['is_allowed'];
    var isAllowed = isAllowedInt == 0 ? false : true;
    String popupMessage = websiteInfo['popup_msg'];
    
    websites[url] = [isSoftBlock, isAllowed, popupMessage];
  }

  cardInfo['websites'] = websites;

  var bannerTitles = [];
  var bannerMessages = [];
  var bannerTriggerTimes = [];

  List dbBannerInfo = db.select('''
  SELECT * FROM banner
  ''');

  for (var bannerInfo in dbBannerInfo) {
    bannerTitles.add(bannerInfo['banner_title']);
    bannerMessages.add(bannerInfo['banner_message']);
    bannerTriggerTimes.add(bannerInfo['trigger_time']);
  }

  cardInfo['banner_titles'] = bannerTitles;
  cardInfo['banner_messages'] = bannerMessages;
  cardInfo['banner_trigger_times'] = bannerTriggerTimes;

  List dbTimeInfo = db.select('''
  SELECT * FROM time
  ''');

  cardInfo['start_time'] = DateTime.parse(dbTimeInfo[0]['start_time']);
  cardInfo['end_time'] = DateTime.parse(dbTimeInfo[0]['end_time']);

  db.dispose();
  return cardInfo;
}

void clear() {
  final db = File(dbFilePath);
  db.deleteSync();
  initialized = false;
}