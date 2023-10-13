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

class LentoDaemon {
  final log = Logger('Class: LentoDaemon');

  void entry() async {
    if (db.mainTimerLoopExists()) {
      log.info('Resuming block after crash...');
      startBlock(newBlock: false);
    } else {
      log.info('Listening for new block data...');
      final daemonServer = await ServerSocket.bind('localhost', 0);
      // saveDaemonPortToSettings(daemonServer.port);
      log.info('DaemonServer on port ${daemonServer.port}.');
      daemonServer.listen(handleConnection);
    }
  }

  void handleConnection(Socket client) {
    log.info('Connected.');

    client.listen((cardInfoData) {
      db.init(path: defaultDBFilePath);

      final cardInfoString = String.fromCharCodes(
        cardInfoData,
      );
      Map cardInfo = json.decode(cardInfoString);
      log.info('Received cardInfo.');

      startBlock(
        newBlock: true,
        apps: cardInfo['apps'],
        websites: cardInfo['websites'],
        duration: cardInfo['blockDuration'],
        banners: cardInfo['banners'],
      );
      client.close();
    }, onError: (error) {
      log.shout(error);
      client.close();
    }, onDone: () {
      log.info('Transmission complete.');
    });
  }

  Future<void> startBlock({
    required bool newBlock,
    Map? apps,
    Map? websites,
    int? duration,
    Map? banners,
  }) async {
    final nullArgs =
        apps == null || websites == null || duration == null || banners == null;
    if (newBlock && nullArgs) {
      throw ArgumentError('New blocks must provide block data!');
    }

    final blockEndTime = duration != null
        ? DateTime.now().add(
            Duration(seconds: duration),
          )
        : db.getEndTime();

    final proxySettings = getPlatformProxySettings();
    final processManager = getPlatformProcessManager();
    final notifManager = NotifManager();
    final appBlocker = AppBlocker(
      processManager: processManager,
      notifManager: notifManager,
    );
    final proxy = LentoProxy(
      proxySettings: proxySettings,
      notifManager: notifManager,
    );
    await proxy.setup();

    if (newBlock && !nullArgs) {
      final bannerQueue = notifManager.buildBannerQueue(banners);
      db.saveAppData(apps);
      db.saveWebsiteData(websites);
      db.saveBannerQueue(bannerQueue);
      db.saveEndTime(blockEndTime);
    }

    Timer.periodic(const Duration(seconds: 1), (timer) {
      print('*******************************');
      var diff = blockEndTime.difference(DateTime.now()).inSeconds;
      log.info('$diff seconds left in block.');
      if (blockEndTime.difference(DateTime.now()).inSeconds > 0) {
        appBlocker.blockApps();
        final bannerQueue = db.getBannerQueue();
        final bannerToFire = notifManager.checkForTriggeredBanners(bannerQueue);
        bannerToFire != null ? notifManager.fireBanner(bannerToFire) : null;
      } else {
        proxy.cleanup();
        db.reset();
        timer.cancel();
        log.info('Block teardown complete.');
      }
    });
  }

  void saveDaemonPortToSettings(int port) async {
    var jsonSettings = await File(lentoSettingsPath).readAsString();
    Map settings = jsonDecode(jsonSettings);
    settings['daemon_port'] = port;
    jsonSettings = json.encode(settings);
    File(lentoSettingsPath).writeAsString(jsonSettings);
  }
}
