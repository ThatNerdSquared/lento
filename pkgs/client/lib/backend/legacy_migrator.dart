import '../config.dart';
import 'card_data.dart';
import 'json_backend.dart';

class LegacyMigrator {
  Map<String, LentoCardData> parseV1(Map contentsMap) {
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

  Map<String, LentoCardData> parseV1_1(Map contentsMap) {
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

  Map<String, LentoCardData> parseV1_2(Map contentsMap) {
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
              reminders: JsonBackend().parseV1Reminders(
                value['scheduledEvents'],
              ),
            ))));
  }
}
