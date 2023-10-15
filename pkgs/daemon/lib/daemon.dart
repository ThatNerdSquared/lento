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
  bool devModeEnabled;

  LentoDaemon({required devMode}) : devModeEnabled = devMode ?? false;

  void entry() async {
    devModeEnabled
        ? log.info('Dev mode enabled. Using alternate notifhelper path.')
        : null;
    if (db.mainTimerLoopExists()) {
      log.info('Resuming block after crash...');
      startBlock();
    } else {
      log.info('Listening for new block data...');
      final daemonServer = await ServerSocket.bind('localhost', 0);
      saveDaemonPortToSettings(daemonServer.port);
      log.info('DaemonServer on port ${daemonServer.port}.');
      daemonServer.listen(handleConnection);
    }
  }

  void handleConnection(Socket client) {
    log.info('Connected.');

    client.listen((cardInfoData) {
      db.init(path: defaultDBFilePath);

      final cardInfoString = String.fromCharCodes(cardInfoData);
      Map cardInfo = json.decode(cardInfoString);
      log.info('Received cardInfo.');

      final bannerQueue = NotifManager.buildBannerQueue(cardInfo['banners']);
      db.saveAppData(cardInfo['apps']);
      db.saveWebsiteData(cardInfo['websites']);
      db.saveBannerQueue(bannerQueue);
      final endTime = DateTime.now().add(
        Duration(seconds: cardInfo['blockDuration']),
      );
      db.saveEndTime(endTime);

      startBlock(endTime: endTime);
      client.close();
    }, onError: (error) {
      log.shout(error);
      client.close();
    }, onDone: () {
      log.info('Transmission complete.');
    });
  }

  Future<void> startBlock({DateTime? endTime}) async {
    final blockEndTime = endTime ?? db.getEndTime();

    final proxySettings = getPlatformProxySettings();
    final processManager = getPlatformProcessManager();
    final notifManager = NotifManager(devModeEnabled: devModeEnabled);
    final appBlocker = AppBlocker(
      processManager: processManager,
      notifManager: notifManager,
    );
    final proxy = LentoProxy(
      proxySettings: proxySettings,
      notifManager: notifManager,
    );
    await proxy.setup();

    Timer.periodic(const Duration(seconds: 1), (timer) {
      print('*******************************');
      final remainingTime = blockEndTime.difference(DateTime.now()).inSeconds;
      log.info('$remainingTime seconds left in block.');
      if (remainingTime > 0) {
        appBlocker.blockApps();
        final bannerQueue = db.getBannerQueue();
        final bannerToFire = notifManager.checkForTriggeredBanners(bannerQueue);
        bannerToFire != null ? notifManager.fireBanner(bannerToFire) : null;
      } else {
        timer.cancel();
        proxy.cleanup();
        db.reset();
        log.info('Block teardown complete.');
      }
    });
  }

  Future<void> saveDaemonPortToSettings(int port) async {
    final settingsFile = File(lentoSettingsPath);
    if (await settingsFile.exists()) {
      final rawJSON = await File(lentoSettingsPath).readAsString();
      final settings = jsonDecode(rawJSON);
      settings['daemonPort'] = port;
      return settingsFile.writeAsStringSync(json.encode(settings));
    }
    await settingsFile.create();
    await settingsFile.writeAsString('{"daemonPort": $port}');
  }
}
