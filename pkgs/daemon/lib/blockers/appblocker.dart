import 'dart:io';
import 'package:logging/logging.dart';
import '../config.dart';

// Class that contains all app-blocking functionality.

/// Below is a summary of blockedApps:
/// {procName : {isSoftBlock: <bool>, lastOpened: <DateTime>, isAllowed: <bool>, popupMessage: <String>}},

class AppBlocker {
  final log = Logger('Class: AppBlocker');
  Map blockedApps = {};

  AppBlocker(this.blockedApps);

  void blockApps() async {
    var hardList = <String>[];
    var softList = <String>[];
    var softBlock = {};
    log.info('appblocker');
    var processes = (await Process.run('ps', [
      '-acxo',
      'pid,comm',
    ]))
        .stdout
        .split('\n');
    log.info('hello');
    processes.removeAt(0);
    processes.removeAt(processes.length - 1);
    log.info(blockedApps);

    for (var rawline in processes) {
      String trimmedLine = rawline.trim();
      var firstSpace = trimmedLine.indexOf(' ');
      var procName = trimmedLine.substring(firstSpace + 1, trimmedLine.length);

      if (blockedApps.containsKey(procName)) {
        log.info('APP: Blocked app $procName detected');
        var app = blockedApps[procName];
        print('app: $app');

        if (!app['isSoftBlock']) {
          log.info('APP: HARD blocked app $procName detected');
          var pid = trimmedLine.substring(0, firstSpace);
          var popupMessage = app['popupMessage'];
          Process.run(notifHelperPath, [
            'banner', // change to popup later
            '$procName hard-blocked',
            'Lento has hard-blocked the app "$procName" during your work session. Your message: $popupMessage'
          ]);
          log.info('APP: HARD: $procName blocked');
          hardList.add(pid);
        } else {
          log.info('APP: SOFT blocked app $procName detected');
          var pid = trimmedLine.substring(0, firstSpace);
          if (!app['isAllowed']) {
            softList.add(pid);
          }
          softBlock[procName] = pid;
        }
      }
    }
    Process.run('kill', hardList);
    Process.run('kill', softList);
    log.info('APP: Blocked apps killed');

    for (var procName in softBlock.keys) {
      var app = blockedApps[procName];
      var diff = DateTime.now().difference(app['lastOpened']).inSeconds;
      print('SOFT BLOCK DIFF: $diff');
      if (app['permClosed'] != true) {
        if (DateTime.now().difference(app['lastOpened']).inSeconds > 15) {
          var isAllowedPopup = Process.runSync(notifHelperPath, [
            'popup',
            '$procName soft-blocked',
            'Lento has soft-blocked the app "$procName" during your work session. Does usage need to be extended by 15 minutes?'
          ]);
          // why does await Process.run not work if Process.runSync works?
          var isAllowedString = isAllowedPopup.stdout.trim();
          var isAllowed = isAllowedString == 'flutter: AlertButton.yesButton';
          print('isAllowed $isAllowed');
          if (isAllowed) {
            log.info('APP: SOFT: extended usage for $procName');
            Process.run('open', ['-a', procName]);
            print('FASHIONITA');
          } else {
            log.info('APP: SOFT: $procName blocked');
            app['permClosed'] = true;
            Process.run(notifHelperPath, [
              'banner',
              '$procName soft-blocked',
              'Lento has blocked the app "$procName" for the rest of your work session.'
            ]);
          }
          app['lastOpened'] = DateTime.now();
          app['isAllowed'] = isAllowed;
        }
      } else {
        Process.run(notifHelperPath, [
          'banner',
          '$procName soft-blocked',
          'Lento has blocked the app "$procName" for the rest of your work session.'
        ]);
      }
    }
  }
}
