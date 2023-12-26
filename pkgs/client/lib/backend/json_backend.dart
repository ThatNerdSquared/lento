import 'dart:io';

import 'package:pret_a_porter/pret_a_porter.dart';

import '../config.dart';
import '../main.dart';
import 'card_data.dart';

class JsonBackend extends PretJsonManager {
  @override
  File get dataFile => File(Config.dataFilePath);
  @override
  String schemaVersion = '1.3.0';
  @override
  Map<String, List<String>> dropFields = {
    '1.2.0': ['goals', 'scheduledEvents']
  };
  @override
  Map get freshJson => {
        'schema': schemaVersion,
        'activatedCard': null,
        'cards': {
          uuID.v4(): LentoCardData.fromDefaults().toJson(),
        },
        'popupMsgs': {},
        'applicationSettings': {
          'theme': AppTheme.system.toString(),
          'defaultRestrictedAccess': false
        },
      };

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
      '1.2.0' => _parseV1_2(contentsMap),
      '1.3.0' => _parseV1_3(contentsMap),
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
      '1.2.0' => Map<String, String>.from(contentsMap['popupMsgs']),
      '1.3.0' => Map<String, String>.from(contentsMap['popupMsgs']),
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
              todos: const {},
              blockedItems: {
                ..._parseV1Sites(value['blockedSites']),
                ..._parseV1Apps(value['blockedApps']),
              },
              reminders: const {},
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
              todos: _parseV1Todos(value['todos']),
              blockedItems: {
                ..._parseV1Sites(value['blockedSites']),
                ..._parseV1Apps(value['blockedApps']),
              },
              reminders: const {},
            ))));
  }

  Map<String, LentoCardData> _parseV1_2(contentsMap) {
    final cardsMap = contentsMap['cards'];
    return Map<String, LentoCardData>.from(
        cardsMap.map((key, value) => MapEntry(
            key,
            LentoCardData(
              cardName: value['name'],
              isActivated: value['isActivated'],
              blockDuration: CardTime.fromPresetTime(value['blockDuration']),
              todos: _parseV1Todos(value['todos']),
              blockedItems: {
                ..._parseV1Sites(value['blockedSites']),
                ..._parseV1Apps(value['blockedApps']),
              },
              reminders: _parseV1Reminders(
                value['scheduledEvents'],
              ),
            ))));
  }

  Map<String, LentoCardData> _parseV1_3(contentsMap) {
    final cardsMap = contentsMap['cards'];
    return Map<String, LentoCardData>.from(
        cardsMap.map((key, value) => MapEntry(
            key,
            LentoCardData(
              cardName: value['name'],
              isActivated: value['isActivated'],
              blockDuration: CardTime.fromPresetTime(value['blockDuration']),
              todos: _parseV1_3Todos(value['todos']),
              blockedItems: _parseV1BlockedItems(value['blockedItems']),
              reminders: _parseV1Reminders(
                value['reminders'],
              ),
            ))));
  }

  Map<String, ReminderData> _parseV1Reminders(seMap) {
    return Map<String, ReminderData>.from(seMap.map(
      (key, value) => MapEntry(
        key,
        ReminderData(
          title: value['title'],
          message: value['message'],
          triggerTimes: value['triggerTimes'],
        ),
      ),
    ));
  }

  Map<String, LentoTodo> _parseV1Todos(todosMap) {
    return Map<String, LentoTodo>.from(todosMap.map(
      (key, value) => MapEntry(
        key,
        LentoTodo(
          title: value['title'],
          completed: value['completed'],
          timeAllocation: 1800,
        ),
      ),
    ));
  }

  Map<String, LentoTodo> _parseV1_3Todos(todosMap) {
    return Map<String, LentoTodo>.from(todosMap.map(
      (key, value) => MapEntry(
        key,
        LentoTodo(
          title: value['title'],
          completed: value['completed'],
          timeAllocation: value['timeAllocation'],
        ),
      ),
    ));
  }

  Map<String, BlockedItemData> _parseV1Sites(blockedSitesMap) {
    return Map<String, BlockedItemData>.from(
        blockedSitesMap.map((key, value) => MapEntry(
              key,
              BlockedItemData(
                type: BlockItemType.website,
                itemName: Uri.parse(value['siteUrl']).path,
                sourcePaths: {'_website': value['siteUrl']},
                isEnabled: value['isEnabled'],
                isRestrictedAccess: value['isRestrictedAccess'],
                customPopupId: value['customPopupId'],
              ),
            )));
  }

  Map<String, BlockedItemData> _parseV1Apps(blockedAppsMap) {
    return Map<String, BlockedItemData>.from(
        blockedAppsMap.map((key, value) => MapEntry(
            key,
            BlockedItemData(
              type: BlockItemType.app,
              itemName: value['appName'],
              sourcePaths: Map<String, String>.from(value['sourcePaths']),
              isEnabled: value['isEnabled'],
              isRestrictedAccess: value['isRestrictedAccess'],
              customPopupId: value['customPopupId'],
            ))));
  }

  Map<String, BlockedItemData> _parseV1BlockedItems(blockedItemsMap) {
    return Map<String, BlockedItemData>.from(
        blockedItemsMap.map((key, value) => MapEntry(
              key,
              BlockedItemData(
                type: convertToBlockItemType(value['type']),
                itemName: value['itemName'],
                sourcePaths: Map<String, String>.from(value['sourcePaths']),
                isEnabled: value['isEnabled'],
                isRestrictedAccess: value['isRestrictedAccess'],
                customPopupId: value['customPopupId'],
              ),
            )));
  }
}
