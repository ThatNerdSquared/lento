import 'package:logging/logging.dart';
import '../config.dart';
import '../notifs.dart';
import 'platform_process_manager.dart';

class BlockedAppItem {
  final bool isRestrictedAccess;
  final String? popupMessage;
  DateTime? lastChallenged;
  bool canBypassRestriction;

  BlockedAppItem({
    required this.isRestrictedAccess,
    required this.popupMessage,
    this.lastChallenged,
    this.canBypassRestriction = false,
  });
}

class AppBlocker {
  final log = Logger('Class: AppBlocker');
  Map<String, BlockedAppItem> blockedApps = {};

  AppBlocker(Map apps)
      : blockedApps = apps.map((key, value) => MapEntry(
              key,
              BlockedAppItem(
                  isRestrictedAccess: value['isRestrictedAccess'],
                  popupMessage: value['popupMessage']),
            ));

  void blockApps() async {
    final detectedRestrictedApps = <ProcessInfo>[];
    final pm = getPlatformProcessManager();
    final processes = pm.rawProcesses();

    for (final rawline in processes) {
      final process = pm.processInfo(rawline);

      if (!blockedApps.containsKey(process.name)) continue;
      final detectedApp = blockedApps[process.name]!;

      if (!detectedApp.canBypassRestriction) {
        pm.killProcess(process);
        if (detectedApp.isRestrictedAccess) {
          log.info('APP: RESTRICTED: restricted app ${process.name} detected');
          detectedRestrictedApps.add(process);
          continue;
        }
        log.info('APP: BLOCKED: ${process.name} blocked');
        showBlockedItemPopup(
          blockedItemName: process.name,
          popupMsg: detectedApp.popupMessage,
        );
      }
    }

    for (final process in detectedRestrictedApps) {
      final detectedApp = blockedApps[process.name]!;
      final invalidRestrictionBypass = !detectedApp.canBypassRestriction ||
          DateTime.now().difference(detectedApp.lastChallenged!).inMinutes >
              restrictionBypassTTL;
      // why does await Process.run not work if Process.runSync works?
      if (invalidRestrictionBypass && !promptUserToUnblock(process.name)) {
        log.info('APP: RESTRICTED: ${process.name} blocked');
        showBlockedItemPopup(
          blockedItemName: process.name,
          popupMsg: detectedApp.popupMessage,
        );
        continue;
      }
      log.info('APP: RESTRICTED: extended usage for ${process.name}');
      detectedApp.lastChallenged = DateTime.now();
      detectedApp.canBypassRestriction = true;
      pm.restartProcess(process);
    }
  }
}
