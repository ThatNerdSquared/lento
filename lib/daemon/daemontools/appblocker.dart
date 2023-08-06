import 'dart:io';

List<String> blockedApps = [];

void checkForBlockedApps() async {
  var killList = <String>[];

  var processes = (await Process.run('ps', [
    '-acxo',
    'pid,comm',
  ]))
      .toString()
      .split('\n');
  processes.removeAt(0);

  for (var rawline in processes) {
    var trimmedLine = rawline.trim();
    var firstSpaceIdx = rawline.indexOf(' ');
    var procName = trimmedLine.substring(firstSpaceIdx, rawline.length);

    if (blockedApps.contains(procName)) {
      killList.add(trimmedLine.substring(0, firstSpaceIdx - 1));
    }
  }
  await Process.run('kill', killList);
}
