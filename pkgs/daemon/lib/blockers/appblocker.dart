import 'package:logging/logging.dart';
import '../config.dart';
import '../db.dart' as db;
import '../notifs.dart';
import 'platform_process_manager.dart';

class AppBlocker {
  final log = Logger('Class: AppBlocker');
  PlatformProcessManager processManager;
  NotifManager notifManager;

  AppBlocker({
    required this.processManager,
    required this.notifManager,
  });

  void blockApps() async {
    final detectedRestrictedApps = <ProcessInfo>[];
    final processes = processManager.rawProcesses();

    for (final rawline in processes) {
      final process = processManager.processInfo(rawline);

      if (db.isNotBlockedApp(process.name)) continue;
      final detectedApp = db.getBlockedApp(process.name);

      if (!detectedApp.canBypassRestriction) {
        processManager.killProcess(process);
        if (detectedApp.isRestrictedAccess) {
          log.info('APP: RESTRICTED: restricted app ${process.name} detected');
          detectedRestrictedApps.add(process);
          continue;
        }
        log.info('APP: BLOCKED: ${process.name} blocked');
        notifManager.showBlockedItemPopup(
          blockedItemName: process.name,
          popupMsg: detectedApp.popupMessage,
        );
      }
    }

    for (final process in detectedRestrictedApps) {
      final detectedApp = db.getBlockedApp(process.name);
      final invalidRestrictionBypass = !detectedApp.canBypassRestriction ||
          DateTime.now().difference(detectedApp.lastChallenged!).inMinutes >
              restrictionBypassTTL;
      // why does await Process.run not work if Process.runSync works?
      if (invalidRestrictionBypass &&
          !notifManager.promptUserToUnblock(process.name)) {
        log.info('APP: RESTRICTED: ${process.name} blocked');
        notifManager.showBlockedItemPopup(
          blockedItemName: process.name,
          popupMsg: detectedApp.popupMessage,
        );
        continue;
      }
      log.info('APP: RESTRICTED: extended usage for ${process.name}');
      db.recordAppChallenge(detectedApp);
      db.setRestrictionBypass(app: detectedApp, canBypassRestriction: true);
      processManager.restartProcess(process);
    }
  }
}
