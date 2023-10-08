import 'dart:io';

import 'config.dart';

enum NotifType { banner, question, popup }

String _callNotifHelper(
  NotifType type,
  String title,
  String msg,
) {
  return (Process.runSync(notifHelperPath, [
    switch (type) {
      NotifType.banner => 'banner',
      NotifType.question => 'question-popup',
      NotifType.popup => 'popup',
    },
    title,
    msg,
  ])).stdout.toString().trim();
}

void showPopup(String title, String msg) {
  _callNotifHelper(NotifType.popup, title, msg);
}

bool promptUserToUnblock(String blockedItemName) {
  final response = _callNotifHelper(
    NotifType.question,
    'Access to $blockedItemName is restricted',
    'Lento has restricted access to "$blockedItemName" during your focus session. Do you need to allow access for 15 minutes?',
  );
  return response == 'flutter: AlertButton.yesButton';
}

void showBlockedItemPopup(
    {required String blockedItemName, String? popupMsg}) async {
  _callNotifHelper(
    NotifType.popup,
    '$blockedItemName blocked',
    'Lento has blocked "$blockedItemName" during your focus session.\n$popupMsg',
  );
}

void showBanner(String title, String msg) {
  _callNotifHelper(NotifType.banner, title, msg);
}
