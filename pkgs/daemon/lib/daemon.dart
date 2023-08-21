import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:logging/logging.dart';
import 'blockers/appblocker.dart';
import 'blockers/proxy_controller.dart';
import 'config.dart' as daemon_config;
import 'db.dart' as db;

Map cardInfo = {};

class LentoDaemon {
  final log = Logger('Class: LentoDaemon');
  final notifHelperPath = './build/macos/Build/Products/Release/LentoNotifHelper.app/Contents/MacOS/LentoNotifHelper "banner" "test" "hw"';
  dynamic task;

  void entry() async {
    db.init();

    if (db.mainTimerLoopExists()) {
      log.info('Resuming block after crash');
      cardInfo = db.buildCardInfo();
      startBlock();
    } else {
      log.info('Listening for cardData for new timerTask');
      final daemonServer = await ServerSocket.bind('localhost', 0);
      saveDaemonPortToSettings(daemonServer.port);
      log.info('DaemonServer on port ${daemonServer.port}');
      daemonServer.listen(handleConnection);
      int blockDuration = cardInfo['block_duration'];
      final blockStartTime = DateTime.now();
      final blockEndTime = blockStartTime.add(Duration(seconds: blockDuration));
      final bannerTriggerTimes = initBannerTriggerTimes();
      cardInfo['block_end_time'] = blockEndTime;
      cardInfo['banner_trigger_times'] = bannerTriggerTimes;
      db.save('card_info', null, cardInfo);
      startBlock();
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

  void startBlock() {
    final startTime = cardInfo['block_start_time'];
    final endTime = cardInfo['block_end_time'];

    final appBlocker = AppBlocker(cardInfo['apps']);
    final proxy = ProxyController(cardInfo['websites']);

    Timer.periodic(const Duration(seconds: 1), (timer) {

    if (startTime.difference(endTime).inSeconds > 0) {
      appBlocker.blockApps();
      proxy.blockWebsites();
      checkBannerTrigger(startTime);
      startTime.add(const Duration(seconds: 1));
      db.save('time', 'block_start_time', startTime);
    } else {
      proxy.cleanup;
      db.clear();
      timer.cancel();
    }
    });
  }

  void saveDaemonPortToSettings(dynamic port) async {
    var jsonSettings = await File(daemon_config.lentoSettingsPath).readAsString();
    Map settings = jsonDecode(jsonSettings);
    settings['daemon_port'] = port;
    jsonSettings = json.encode(settings);
    File(daemon_config.lentoSettingsPath).writeAsString(jsonSettings);
  }

  void checkBannerTrigger(DateTime startTime) {
    List bannerTitles = cardInfo['banner_titles'];
    List bannerMessages = cardInfo['banner_messages'];
    List bannerTriggerTimes = cardInfo['banner_trigger_times'];
    var bannerTitle = bannerTitles[0];
    var bannerMessage = bannerMessages[0];
    if (startTime.difference(bannerTriggerTimes[0]).inSeconds <= 1) {
      stdout.write('$notifHelperPath "banner" "$bannerTitle" "$bannerMessage"');
    }

    cardInfo['banner_titles'] = bannerTitles.removeAt(0);
    cardInfo['banner_messages'] = bannerTriggerTimes.removeAt(0);
    cardInfo['banner_trigger_times'] = bannerTriggerTimes.removeAt(0);
  }

  List initBannerTriggerTimes() {
    var bannerTriggerTimes = [];
    for (int interval in cardInfo['banner_trigger_time_intervals']) {
      bannerTriggerTimes.add(DateTime.now().add(Duration(seconds: interval)));
    } 

    return bannerTriggerTimes;
  }
}

void main(){
  Logger.root.level = Level.ALL; // defaults to Level.INFO
  Logger.root.onRecord.listen((record) {
    print('${record.level.name}: ${record.time}: ${record.message}');
  });
  LentoDaemon().entry();
}