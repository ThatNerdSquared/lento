import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:flutter_platform_alert/flutter_platform_alert.dart';
import 'package:windows_notification/notification_message.dart';
import 'package:windows_notification/windows_notification.dart';

void main(List<String> args) async {
  // init behind-the-scenes flutter things
  WidgetsFlutterBinding.ensureInitialized();

  // parse args
  String notifType;
  String? customMessage;
  String? customTitle;

  switch (args.length) {
    case 1:
      notifType = args[0];
      break;
    case 2:
      notifType = args[0];
      customMessage = args[1];
    case 3:
      notifType = args[0];
      customMessage = args[1];
      customTitle = args[2];
    default:
      // ignore: avoid_print
      print('Error parsing args!');
      exit(1);
  }

  switch (notifType) {
    case "banner":
      if (Platform.isMacOS) {
        await showBanner(customMessage, customTitle);
      } else if (Platform.isWindows) {
        await showWinBanner(customMessage, customTitle);
      }
      break;
    case "popup":
      await showPopup(customMessage, customTitle, false);
    case "question-popup":
      await showPopup(customMessage, null, true);
    default:
      exit(0);
  }
}

Future<void> showPopup(String? customMessage, String? customTitle, isQuestion) async {
  final clickedButton = await FlutterPlatformAlert.showAlert(
    windowTitle: customTitle ?? "_defaultTitle",
    text: customMessage ?? "_defaultMessage",
    alertStyle: isQuestion ? AlertButtonStyle.yesNoCancel : AlertButtonStyle.ok,
    iconStyle: IconStyle.information,
  );
  // ignore: avoid_print
  print(clickedButton);
  exit(0);
}

Future<void> showBanner(String? customMessage, String? customTitle) async {
  final flutterLocalNotificationsPlugin = FlutterLocalNotificationsPlugin();
  const InitializationSettings initializationSettings = InitializationSettings(
    macOS: DarwinInitializationSettings(),
  );
  await flutterLocalNotificationsPlugin.initialize(
    initializationSettings,
  );
  await flutterLocalNotificationsPlugin
      .resolvePlatformSpecificImplementation<
          MacOSFlutterLocalNotificationsPlugin>()
      ?.requestPermissions(
        alert: true,
        badge: true,
        sound: true,
      );
  // DO NOT REMOVE THIS VARIABLE DECLARATION, IT FORCES
  // AN AWAIT TO ENSURE THE BANNER SHOWS PROPERLY
  // ignore: unused_local_variable
  final test = await flutterLocalNotificationsPlugin.show(
      0, customTitle ?? 'Keep focused!', customMessage ?? '', null,
      payload: 'item x');
  exit(0);
}

Future<void> showWinBanner(String? customMessage, String? customTitle) {
  // REMOVE THIS COMMENTED OUT STUFF AFTER WINDOWS TESTING IS COMPLETE
  // final _winNotifyPlugin = WindowsNotification(
  //   applicationId: "r"{D65231B0-B2F1-4857-A4CE-A8E7C6EA7D27}\WindowsPowerShell\v1.0\powershell.exe""
  // );
  final winNotifyPlugin = WindowsNotification(applicationId: null);
  final message = NotificationMessage.fromPluginTemplate(
    "notif1",
    customTitle ?? "Keep focused!",
    customMessage ?? "",
  );

  winNotifyPlugin.showNotificationPluginTemplate(message);
  exit(0);
}
