import 'dart:ffi';
import 'dart:io';

import 'package:path/path.dart';
import 'package:sqlite3/sqlite3.dart';

import '../../daemon_config.dart';
bool intialized = false;

void init() {
  if (intialized != true) {
    var db = sqlite3.open(dbFilePath);
    print('hello');
    db.execute('''
      CREATE TABLE BlockItems(
        owner varchar(100),
        isSoftBlock int,
        allowInterval int,
        lastAsked datetime,
        isAllowed int,
        popupMsg varchar(100)
      );
      
      CREATE TABLE AppBlockItems(
        procName varchar(100)
      );

      CREATE TABLE WebsiteBlocksItems(
        websiteUrl varchar(100)
      );

      CREATE TABLE NotificationItems(
        owner varchar(100),
        message varchar(100),
        interval float
      );

      CREATE TABLE TimerTasks(
        name varchar(100),
        endTIme datetime
      );

    ''');

    db.dispose();
    intialized = true;
  }
}

List getAllTimerTasks() {
  var db = sqlite3.open(dbFilePath);
  List timerTasks = db.select('SELECT * FROM TimerTasks');
  db.dispose();

  List taskList = [];

  for(int i = 0; i <= timerTasks.length - 1; i ++) {
    var task = buildTimerTask(timerTasks[i]);
    taskList.add(task); // 0 is task
  }

  return taskList;

}

List buildTimerTask(task) {
  List timerTask = [];
  return timerTask;
}