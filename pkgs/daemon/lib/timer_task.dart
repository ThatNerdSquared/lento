import 'dart:async';
import 'package:logging/logging.dart';
import 'blockers/appblocker.dart';
import 'blockers/proxy_controller.dart';
import 'daemontools/db.dart' as db;

// class that triggers all blocking and timing for apps/websites when a block starts

class TimerTask{
  final log = Logger('Class: TimerTask');
  String test = '';
  String name = '';
  int taskInterval = 0;
  dynamic appBlocker; // change type later
  dynamic proxy; // change type later
  Map appBlockItems = {};
  Map websiteBlockItems = {};

  TimerTask(Map cardInfo){
    // cardInfo: {name: cardName, taskInterval: seconds, apps: [list of procnames], websites: [list of urls]}
    name = cardInfo['name'];
    taskInterval = cardInfo['taskInterval'];
    appBlockItems = appBlockItemConverter(cardInfo['apps']);
    websiteBlockItems = siteBlockItemConverter(cardInfo['websites']);
    appBlocker = AppBlocker(appBlockItems);
    proxy = ProxyController(websiteBlockItems);
  }

  TimerTask.init(this.name, this.taskInterval, this.appBlocker, this.proxy, this.appBlockItems, this.websiteBlockItems);


  void start(TimerTask task){
    log.info('Starting main timer and block');
    db.saveTimerTask(task);
    startTimer(task.taskInterval);

    // notif logic

    db.saveTimerTask(task);
    log.info('Task started');

  }

  void printBlockData() {
    print('filler');
  }

  void startTimer(int time) {
    Timer.periodic(const Duration(seconds : 1), (timer) {

      if (time != 0) {
        appBlocker.blockApps(appBlockItems);
        time -= 1;
      } else {
        cleanup();
        timer.cancel();
      }
     });
  }

  Map appBlockItemConverter (Map cardInfo) {
    return cardInfo;
  }

  Map siteBlockItemConverter (Map cardInfo) {
    return cardInfo;
  }


  void cleanup(){
    
  }

}