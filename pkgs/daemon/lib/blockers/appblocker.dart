import 'dart:io';
import 'package:logging/logging.dart';
import '../config.dart';

// Class that contains all app-blocking functionality.

/// Below is a summary of blockedApps:
/// {procName : {isSoftBlock: <bool>, lastOpened: <DateTime>, isAllowed: <bool>, popupMsg: <String>}},

class AppBlocker {
  final log = Logger('Class: AppBlocker');
  Map blockedApps = {};

  AppBlocker(blockedApps) {
    this.blockedApps;
  }

  void blockApps() async {
    var killList = <String>[];

    var processes = (await Process.run('ps', [
      '-acxo',
      'pid,comm',
    ]))
        .stdout
        .split('\n');
    processes.removeAt(0);
    processes.removeAt(processes.length - 1);

    for (var rawline in processes) {
      var trimmedLine = rawline.trim();
      var firstSpace = trimmedLine.indexOf(' ');
      var procName = trimmedLine.substring(firstSpace + 1, trimmedLine.length);

      if (blockedApps.containsKey(procName)) {
        log.info('APP: Blocked app $procName detected');
        var app = blockedApps[procName];

        if (!app['isSoftBlock']) {
          log.info('APP: HARD blocked app $procName detected');
          var pid = trimmedLine.substring(0, firstSpace - 1);
          killList.add(pid);
          var popupMessage = app['popupMessage'];
          await Process.run(notifHelperPath, [
            'popup',
            '$procName hard-blocked',
            'Lento has hard-blocked the app "$procName" during your work session. Your message: $popupMessage'
          ]);
        } else {
          log.info('APP: SOFT blocked app $procName detected');
          if (DateTime.now().difference(app['lastOpened']).inMinutes > 15) {
            var pid = trimmedLine.substring(0, firstSpace - 1);
            await Process.run('kill', [pid]);
            String isAllowedString = (await Process.run(notifHelperPath, [
              'popup',
              '$procName soft-blocked',
              'Lento has soft-blocked the app "$procName" during your work session. Does usage need to be extended by 15 minutes?'
            ]))
                .stdout();
            var isAllowed = isAllowedString == 'flutter: AlertButton.yesButton'
                ? true
                : false;
            if (isAllowed) {
              log.info('APP: SOFT: extended usage for $procName');
              await Process.run('open', ['a', procName]);
            } else {
              log.info('APP: SOFT: $procName blocked');
            }

            app['lastOpened'] = DateTime.now();
            app['isAllowed'] = isAllowed;
          }
        }
      }
    }
    await Process.run('kill', killList);
    log.info('APP: HARD: app blocked');
  }
}
