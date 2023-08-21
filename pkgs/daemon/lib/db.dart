import 'dart:io';
import 'package:collection/collection.dart';
import 'package:logging/logging.dart';
import 'package:sqlite3/sqlite3.dart';
import 'config.dart';

bool intialized = false;
final log = Logger('File: DB');

/// Below is a summary of the information cardInfo stores.
/// Keys with asterisks next to them denotes info that is only needed when a block starts for the first time.
/// Keys with tildas next to them denotes info that is needed only needed when a block restarts/info that is created as the daemon executes.
///
/// cardInfo {
/// <String> apps : {<String> proc_name : [<bool> is_soft_block, <bool> is_allowed, <String> popup_msg]},
/// <String> websites : {<String> url: [<bool> is_soft_block, <bool> is_allowed, <String> popup_msg]},
/// <String> banner_messages : [<String>], (only used in daemon.dart, not needed in db)
/// <String> banner_trigger_times : [<DateTime>]
/// *<String> blockDuration : <int>,
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
  if (!intialized) {
    checkForDB();
    var db = sqlite3.open(dbFilePath);
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
        banner_message varchar(100),
        trigger_time varchar(50)
      );

      CREATE TABLE time(
        start_time varchar(50),
        end_time varchar(50)
      );

    ''');

    db.dispose();
    intialized = true;
  }
}


bool mainTimerLoopExists(){
  bool exists;
  var db = sqlite3.open(dbFilePath);

  if (db.select('SELECT count(*) FROM MainTimerLoop').isEmpty) {
    exists = false;
  } else {
    exists = true;
  }

  db.dispose();

  return exists;
}

void save(String table, dynamic row, dynamic data) {
  var db = sqlite3.open(dbFilePath);
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

    List bannerMessages = cardInfo['banner_messages'].value;
    List bannerTriggerTimes = cardInfo['banner_trigger_times'].value;

    for (var pair in IterableZip<dynamic>([bannerMessages, bannerTriggerTimes])) { 
      // save banner messages and banner trigger times to db
      String bannerMessage = pair[0];
      var bannerTriggerTime = pair[1].toString();

      db.execute('''
      INSERT INTO banner (banner_message, trigger_time)
      VALUES ($bannerMessage, $bannerTriggerTime);
      ''');
    }

    final startTime = cardInfo['block_start_time'];
    final endTime = cardInfo['block_end_time'];

    db.execute('''
    INSERT INTO time (start_time, end_time)
    VALUES ($startTime, $endTime)
    ''');

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
  final cardInfo = {};
  
  return cardInfo;
}

void clear() {

}

