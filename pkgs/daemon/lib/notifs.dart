import 'dart:io';

import 'package:clock/clock.dart';
import 'package:logging/logging.dart';
import 'package:meta/meta.dart';

import 'config.dart';
import 'db.dart' as db;

enum NotifType { banner, question, popup }

@immutable
class BannerNotif {
  final String title;
  final String message;
  final DateTime triggerTime;

  const BannerNotif({
    required this.title,
    required this.message,
    required this.triggerTime,
  });
}

class NotifManager {
  final log = Logger('NotifManager');

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

  bool promptUserToUnblock(String blockedItemName) {
    final response = _callNotifHelper(
      NotifType.question,
      'Access to $blockedItemName is restricted',
      'Lento has restricted access to "$blockedItemName" during your focus session. Do you need to allow access for 15 minutes?',
    );
    return response == 'flutter: AlertButton.yesButton';
  }

  void showBlockedItemPopup({
    required String blockedItemName,
    required String? popupMsg,
  }) async {
    _callNotifHelper(
      NotifType.popup,
      '$blockedItemName blocked',
      'Lento has blocked "$blockedItemName" during your focus session.\n$popupMsg',
    );
  }

  void fireBanner(BannerNotif banner) {
    _callNotifHelper(NotifType.banner, banner.title, banner.message);
  }

  List<BannerNotif> buildBannerQueue(Map banners) {
    final bannerQueue = <BannerNotif>[];
    for (final banner in banners.values) {
      for (final triggerTime in banner['triggerTimes']) {
        bannerQueue.add(BannerNotif(
            title: banner['title'],
            message: banner['message'],
            triggerTime: clock.now().add(Duration(seconds: triggerTime))));
      }
    }
    bannerQueue.sort((a, b) => a.triggerTime.compareTo(b.triggerTime));
    return bannerQueue;
  }

  BannerNotif? checkForTriggeredBanners(List<BannerNotif> bannerQueue) {
    if (bannerQueue.isEmpty ||
        clock.now().difference(bannerQueue[0].triggerTime).inSeconds < 0) {
      return null;
    }
    log.info('Found banner to fire...');
    db.popBannerOffQueue();
    return bannerQueue[0];
  }
}
