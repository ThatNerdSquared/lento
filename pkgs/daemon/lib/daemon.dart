import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:logging/logging.dart';
import 'blockers/appblocker.dart';
import 'blockers/proxy_controller.dart';
import 'config.dart' as daemon_config;
import 'db.dart' as db;


/// Below is a summary of the information cardInfo stores.

/// cardInfo {
/// apps : {proc_name : {is_soft_block: <bool>, is_allowed: <bool>, popup_msg: <String>}},
/// websites : {url: {is_soft_block: <bool>, is_allowed: <bool>, popup_msg: <String>}},
/// bannerText : [{bannerTitle: bannerMessage}],
/// blockDuration : <int>,
/// bannerTriggerTimeIntervals : [<int>], ** only used/exists when new block starts (cardInfo is sent from gui)
/// banenrTriggerTimes: [<DateTime>] ** only used/exists when a block is restarting (cardInfo is rebuilt frm DB)
/// }
/// 

class LentoDaemon {
  final log = Logger('Class: LentoDaemon');
  final notifHelperPath = 'placeholder';


  void entry() async {
    if (db.mainTimerLoopExists()) {
      log.info('Resuming block after crash');
      final cardInfo = db.buildCardInfo();

      final blockStartTime = DateTime.now();
      final blockEndTime = blockStartTime.add(Duration(seconds: cardInfo['blockDuration']));
      final bannerTriggerTimes = cardInfo['bannerTriggerTimes'];
      // ignore: unused_local_variable

      startBlock(cardInfo['apps'], cardInfo['websites'], blockEndTime, cardInfo['bannerInfo'], bannerTriggerTimes);
  
    } else {
      db.init();
      log.info('Listening for cardData for new timerTask');
      final daemonServer = await ServerSocket.bind('localhost', 0);
      saveDaemonPortToSettings(daemonServer.port);
      log.info('DaemonServer on port ${daemonServer.port}');
      daemonServer.listen(handleConnection);
    }
  }

  void handleConnection(Socket client) {
    log.info('GUI connected');

    client.listen((cardInfoData) {

      final cardInfoString = String.fromCharCodes(cardInfoData); // convert bytes to string to map (cardInfo)
      log.info('Recieved cardInfo');
      Map cardInfo = json.decode(cardInfoString);

      final blockStartTime = DateTime.now();
      final blockEndTime = blockStartTime.add(Duration(seconds: cardInfo['blockDuration']));
      final bannerTriggerTimes = initBannerTriggerTimes(cardInfo['bannerTriggerTimeIntervals']);
      // ignore: unused_local_variable
      
      db.saveAppData(cardInfo['apps']);
      db.saveWebsiteData(cardInfo['websites']);
      db.saveBannerData(cardInfo['bannerInfo'], bannerTriggerTimes);
      db.saveTime(blockEndTime);

      startBlock(cardInfo['apps'], cardInfo['websites'], blockEndTime, cardInfo['bannerInfo'], bannerTriggerTimes);

      client.close();
    }, onError: (error) {
      log.shout(error);

      client.close();
    }, onDone: () {
      log.info('GUI offline');
    });
  }

  void startBlock(Map apps, Map websites, DateTime endTime, List bannerInfo, List bannerTriggerTimes) {

    final appBlocker = AppBlocker(apps);
    final proxy = ProxyController(websites);

    Timer.periodic(const Duration(seconds: 1), (timer) {
      if (DateTime.now().difference(endTime).inSeconds > 0) {
        appBlocker.blockApps();
        checkBannerTrigger(bannerInfo, bannerTriggerTimes);
      } else {
        proxy.cleanup();
        db.clear();
        timer.cancel();
      }
    });
  }

  void saveDaemonPortToSettings(dynamic port) async {
    var jsonSettings =
        await File(daemon_config.lentoSettingsPath).readAsString();
    Map settings = jsonDecode(jsonSettings);
    settings['daemon_port'] = port;
    jsonSettings = json.encode(settings);
    File(daemon_config.lentoSettingsPath).writeAsString(jsonSettings);
  }

  List initBannerTriggerTimes(List bannerTriggerTimeIntervals) {
    var bannerTriggerTimes = [];
    for (int interval in bannerTriggerTimeIntervals) {
      bannerTriggerTimes.add(DateTime.now().add(Duration(seconds: interval)));
    }

    return bannerTriggerTimes;
  }

  void checkBannerTrigger(List bannerInfo, List bannerTriggerTimes) {
    String bannerTitle = bannerInfo[0].keys.elementAt(0);
    String bannerMessage = bannerInfo[0][bannerTitle];
    DateTime bannerTriggerTime = bannerTriggerTimes[0];

    if (DateTime.now().difference(bannerTriggerTime).inSeconds <= 1) {
      Process.run(notifHelperPath, ['banner', bannerTitle, bannerMessage]);
    }

    bannerInfo.removeAt(0);
    bannerTriggerTimes.removeAt(0);

  }
}

void main() {
  Logger.root.level = Level.ALL; // defaults to Level.INFO
  Logger.root.onRecord.listen((record) {
    print('${record.level.name}: ${record.time}: ${record.message}');
  });
  LentoDaemon().entry();
}
