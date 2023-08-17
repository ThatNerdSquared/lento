import 'dart:convert';
import 'dart:io';
import 'package:logging/logging.dart';
import 'config.dart' as daemon_config;
import 'daemontools/db.dart' as db;
import 'timer_task.dart' as timer_task;

class LentoDaemon {
  final log = Logger('Class: LentoDaemon');
  Map cardInfo = {};
  dynamic task;

  void entry() async {
    db.init();

    timer_task.TimerTask? dbTimerTask = db.getTimerTask();

    // below comment makes linter happy, otherwise returns 
    // unnecesscary_null_comparison even though the null comparison is necesscary...

    // ignore: unnecessary_null_comparison
    if (dbTimerTask != null) { // daemon is killed while block ongoing
      log.info('Resuming block after crash');
      dbTimerTask.start(dbTimerTask);
    } else { // new block
      // listen to messages coming from gui
      log.info('Listening for cardData for new timerTask');
      final daemonServer = await ServerSocket.bind('localhost', 0);
      saveDaemonPortToSettings(daemonServer.port);
      log.info('DaemonServer on port ${daemonServer.port}');
      daemonServer.listen(handleConnection);
      startBlock(cardInfo);
    }

  }

  void handleConnection(Socket client) {
    log.info('GUI connected');

    client.listen(
      (cardInfoData){ // convert bytes to string to map
        final cardInfoString = String.fromCharCodes(cardInfoData);
        log.info('Recieved cardInfo');
        cardInfo = json.decode(cardInfoString);

        client.close();
      },

      onError: (error){
        log.shout(error);

        client.close();
      },

      onDone: (){
        log.info('GUI offline');
      }
    );

  }

  void startBlock(Map cardInfo) {
    task = timer_task.TimerTask(cardInfo);
    task.init;
    task.start(task);
    log.info('Starting block: ${task.name}');
    task.printBlockData();
  }

  void saveDaemonPortToSettings(dynamic port) async {
    var jsonSettings = await File(daemon_config.lentoSettingsPath).readAsString();
    var settingsMap = jsonDecode(jsonSettings);
    settingsMap['daemon_port'] = port;
    jsonSettings = json.encode(settingsMap);
    File(daemon_config.lentoSettingsPath).writeAsString(jsonSettings);
  }
}

void main(){
  Logger.root.level = Level.ALL; // defaults to Level.INFO
  Logger.root.onRecord.listen((record) {
    print('${record.level.name}: ${record.time}: ${record.message}');
  });
  LentoDaemon().entry();
}