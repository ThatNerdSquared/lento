import 'dart:io';

import 'package:pret_a_porter/pret_a_porter.dart';

import '../config.dart';
import '../main.dart';
import 'card_data.dart';

class JsonBackend extends PretJsonManager {
  @override
  File get dataFile => File(Config.dataFilePath);
  @override
  String schemaVersion = '1.1.0';
  @override
  Map get freshJson => {
        'schema': schemaVersion,
        'activatedCard': null,
        'cards': {
          uuID.v4(): const LentoCardData.fromDefaults().toJson(),
        },
        'popupMsgs': {},
        'scheduledEvents': {},
        'goals': {},
        'applicationSettings': {
          'theme': AppTheme.system.toString(),
          'defaultRestrictedAccess': false
        },
      };

  void writeDeckToJson(Map<String, LentoCardData> cardsToWrite) {
    jsonWriteWrapper((initialData) {
      final mappifiedCards = cardsToWrite.map((key, value) => MapEntry(
            key,
            value.toJson(),
          ));
      initialData['cards'] = mappifiedCards;
      return initialData;
    });
  }

  void writePopupMsgsToJson(Map<String, String> msgsToWrite) {
    jsonWriteWrapper((initialData) {
      initialData['popupMsgs'] = msgsToWrite;
      return initialData;
    });
  }

  Map<String, LentoCardData> readDeckFromJson() {
    final contentsMap = pretLoadJson();
    return switch (contentsMap['schema']) {
      '1.0.0' => _parseV1(contentsMap),
      '1.1.0' => _parseV1_1(contentsMap),
      _ => throw UnsupportedError(
          'Invalid schema version "${contentsMap['schema']}"',
        ),
    };
  }

  Map<String, String> readPopupMsgsFromJson() {
    final contentsMap = pretLoadJson();
    return switch (contentsMap['schema']) {
      '1.0.0' => Map<String, String>.from(contentsMap['popupMsgs']),
      '1.1.0' => Map<String, String>.from(contentsMap['popupMsgs']),
      _ => throw UnsupportedError(
          'Invalid schema version "${contentsMap['schema']}"',
        )
    };
  }

  Map<String, LentoCardData> _parseV1(contentsMap) {
    final cardsMap = contentsMap['cards'];
    return Map<String, LentoCardData>.from(
        cardsMap.map((key, value) => MapEntry(
            key,
            LentoCardData(
              cardName: value['name'],
              isActivated: value['isActivated'],
              blockDuration: CardTime.fromPresetTime(value['blockDuration']),
              blockedSites: _parseV1Sites(value['blockedSites']),
              blockedApps: _parseV1Apps(value['blockedApps']),
              todos: const {},
            ))));
  }

  Map<String, LentoCardData> _parseV1_1(contentsMap) {
    final cardsMap = contentsMap['cards'];
    return Map<String, LentoCardData>.from(
        cardsMap.map((key, value) => MapEntry(
            key,
            LentoCardData(
              cardName: value['name'],
              isActivated: value['isActivated'],
              blockDuration: CardTime.fromPresetTime(value['blockDuration']),
              blockedSites: _parseV1Sites(value['blockedSites']),
              blockedApps: _parseV1Apps(value['blockedApps']),
              todos: _parseV1Todos(value['todos']),
            ))));
  }

  Map<String, LentoTodo> _parseV1Todos(todosMap) {
    return Map<String, LentoTodo>.from(todosMap.map(
      (key, value) => MapEntry(
        key,
        LentoTodo(
          title: value['title'],
          completed: value['completed'],
        ),
      ),
    ));
  }

  Map<String, BlockedWebsiteData> _parseV1Sites(blockedSitesMap) {
    return Map<String, BlockedWebsiteData>.from(
        blockedSitesMap.map((key, value) => MapEntry(
              key,
              BlockedWebsiteData(
                siteUrl: Uri.parse(value['siteUrl']),
                isEnabled: value['isEnabled'],
                isRestrictedAccess: value['isRestrictedAccess'],
                customPopupId: value['customPopupId'],
              ),
            )));
  }

  Map<String, BlockedAppData> _parseV1Apps(blockedAppsMap) {
    return Map<String, BlockedAppData>.from(
        blockedAppsMap.map((key, value) => MapEntry(
            key,
            BlockedAppData(
              appName: value['appName'],
              sourcePaths: Map<String, String>.from(value['sourcePaths']),
              isEnabled: value['isEnabled'],
              isRestrictedAccess: value['isRestrictedAccess'],
              customPopupId: value['customPopupId'],
            ))));
  }
}
