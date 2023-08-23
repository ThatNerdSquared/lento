import 'dart:io';
import '../config.dart';

// Class that contains all app-blocking functionality.

/// Below is a summary of blockedApps: 
/// {procName : {isSoftBlock: <bool>, lastOpened: <DateTime>, isAllowed: <bool>, popupMsg: <String>}},

class AppBlocker {
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
        var app = blockedApps[procName];

        if (!app['isSoftBlock']) {
          var pid = trimmedLine.substring(0, firstSpace - 1);
          killList.add(pid);
          var popupMessage = app['popupMessage'];
          await Process.run(notifHelperPath, ['popup', procName, 'Lento has hard-blocked the app "$procName" during your work session. Your message: $popupMessage']);
        } else {
          if (DateTime.now().difference(app['lastOpened']).inMinutes > 15) {
            var pid = trimmedLine.substring(0, firstSpace - 1);
            await Process.run('kill', [pid]);
            bool isAllowed = (await Process.run(notifHelperPath, ['popup', procName, 'Lento has soft-blocked the app "$procName" during your work session. Does usage need to be extended by 15 minutes?'])).stdout();
             // fix procName issue and convert to bool issue
            
            if (isAllowed) {
              await Process.run('open', ['a', procName]);
              // fix procName issue
            }

            app['lastOpened'] = DateTime.now();
            app['isAllowed'] = isAllowed;

          }
        }
      }
    }
    await Process.run('kill', killList);
  }
}
