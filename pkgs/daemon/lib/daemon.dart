import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:logging/logging.dart';
import 'blockers/appblocker.dart';
import 'blockers/platform_process_manager.dart';
import 'blockers/platform_proxy_settings.dart';
import 'blockers/proxy.dart';
import 'config.dart';
import 'db.dart' as db;
import 'notifs.dart';

/// Below is a summary of the information cardInfo stores.

/// cardInfo {
/// apps : {procName : {isSoftBlock: <bool>, lastOpened: <DateTime>, isAllowed: <bool>, popupMessage: <String>}},
/// websites : {url: {isSoftBlock: <bool>, lastOpened: <DateTime>, isAllowed: <bool>, popupMessage: <String>}},
/// bannerText : [{bannerTitle: bannerMessage}],
/// blockDuration : <int>, ** only used/exists when new block starts (exists when cardInfo is sent from gui)
/// bannerTriggerTimeIntervals : [<int>], ** only used/exists when new block starts (exists when cardInfo is sent from gui)
/// bannerTriggerTimes: [<DateTime>] ** only used/exists when a block is restarting (exists when cardInfo is rebuilt from DB)
/// }
///
/// lastOpened is set to DateTime.min() when cardInfo is received from GUI.

class LentoDaemon {
  final log = Logger('Class: LentoDaemon');

  void entry() async {
    if (await db.checkForDB()) {
      log.info('Resuming block after crash');

      final apps = db.buildAppInfo();
      final websites = db.buildWebsiteInfo();
      final blockEndTime = db.buildTimeInfo();
      final bannerInfo = db.buildBannerInfo();
      final banners = bannerInfo[0];

      startBlock(apps, websites, blockEndTime, banners);
    } else {
      log.info('Listening for cardData for new block');
      final daemonServer = await ServerSocket.bind('localhost', 0);
      // saveDaemonPortToSettings(daemonServer.port);
      log.info('DaemonServer on port ${daemonServer.port}');
      daemonServer.listen(handleConnection);
    }
  }

  void handleConnection(Socket client) {
    log.info('GUI connected');

    client.listen((cardInfoData) {
      final dbFile = File(dbFilePath);
      dbFile.create();
      db.init();

      final cardInfoString = String.fromCharCodes(
          cardInfoData); // convert bytes to string to map (cardInfo)
      log.info('Recieved cardInfo');
      Map cardInfo = json.decode(cardInfoString);

      final blockStartTime = DateTime.now();
      final blockEndTime =
          blockStartTime.add(Duration(seconds: cardInfo['blockDuration']));

      print(cardInfo);
      print(cardInfo['apps']['Spotify']['isSoftBlock']);
      print(cardInfo['apps']['Spotify']['isSoftBlock'].runtimeType);

      /*
      db.saveAppData(cardInfo['apps']);
      db.saveWebsiteData(cardInfo['websites']);
      db.saveBannerData(cardInfo['bannerText'], bannerTriggerTimes);
      db.saveTime(blockEndTime);
      */

      startBlock(cardInfo['apps'], cardInfo['websites'], blockEndTime,
          cardInfo['banners']);
      client.close();
    }, onError: (error) {
      log.shout(error);
      client.close();
    }, onDone: () {
      log.info('GUI offline');
    });
  }

  Future<void> startBlock(
    Map apps,
    Map websites,
    DateTime endTime,
    Map banners,
  ) async {
    print(apps);

    final proxySettings = getPlatformProxySettings();
    final processManager = getPlatformProcessManager();
    final notifManager = NotifManager();
    final appBlocker = AppBlocker(
      apps: apps,
      processManager: processManager,
      notifManager: notifManager,
    );
    final proxy = LentoProxy(
      websites: websites,
      proxySettings: proxySettings,
      notifManager: notifManager,
    );
    await proxy.setup();
    final bannerQueue = notifManager.buildBannerQueue(banners);
    db.saveBannerQueue(bannerQueue);

    Timer.periodic(const Duration(seconds: 1), (timer) {
      print('*******************************');
      var diff = endTime.difference(DateTime.now()).inSeconds;
      print('timeDiff: $diff');
      if (endTime.difference(DateTime.now()).inSeconds > 0) {
        appBlocker.blockApps();
        final bannerQueue = db.getBannerQueue();
        final bannerToFire = notifManager.checkForTriggeredBanners(bannerQueue);
        bannerToFire != null ? notifManager.fireBanner(bannerToFire) : null;
        //db.saveAppData(apps);
        //db.saveWebsiteData(websites);
        //db.saveBannerData(bannerText, bannerTriggerTimes);
      } else {
        proxy.cleanup();
        db.reset();
        timer.cancel();
        print('sup');
      }
    });
  }

  void saveDaemonPortToSettings(dynamic port) async {
    var jsonSettings = await File(lentoSettingsPath).readAsString();
    Map settings = jsonDecode(jsonSettings);
    settings['daemon_port'] = port;
    jsonSettings = json.encode(settings);
    File(lentoSettingsPath).writeAsString(jsonSettings);
  }
}
