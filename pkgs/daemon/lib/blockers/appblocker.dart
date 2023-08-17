import 'dart:io';

// class that contains all app-blocking functionality

class AppBlocker {
  dynamic blockedAppItemsMap; // change type later

  AppBlocker(blockedAppItemsMap) {
    this.blockedAppItemsMap;
  }
  // blockedAppsMap contains procName: AppItem

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

      if (blockedAppItemsMap.containsKey(procName)) {
        var appItem = blockedAppItemsMap[procName];

        if (!appItem.isSoftBlock) {
          var pid = trimmedLine.substring(0, firstSpace - 1);
          killList.add(pid);
        } else {
          if (DateTime.now().difference(appItem.lastOpened).inSeconds > appItem.allowInterval) {
            var pid = trimmedLine.substring(0, firstSpace - 1);
            await Process.run('kill', [pid]);

            // NotifsContoller, popupAppAllow

            appItem.lastOpened = DateTime.now();
            
            //app.popupAppAllow
            // DBController update app record
          } else {
            // if app is not allowed, block
          }   
        }
      }
    }
    await Process.run('kill', killList);
  }

  // Map generateAppMap(Map blockedAppMap, {bool softBlock = false}){
  //   var appMap = {};

  //   for(var procName in blockedAppMap.keys) {
  //     var appItem = blockedAppMap[procName];

  //   }
  //   return appMap;
  // }
}