import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:pret_a_porter/pret_a_porter.dart';

import '../config.dart';
import '../main.dart';
import 'json_backend.dart';

/// Class that controls a list of [LentoCardData].
class LentoDeck extends StateNotifier<Map<String, LentoCardData>> {
  LentoDeck({
    Map<String, LentoCardData>? initialDeck,
  }) : super(initialDeck ?? <String, LentoCardData>{}) {
    readDeck();
  }

  void _findAndModifyCardAttribute(
    String cardId,
    Function(LentoCardData oldCard) modifierCallback,
  ) {
    state = state.map((key, value) {
      if (key == cardId) {
        return MapEntry(key, modifierCallback(value));
      } else {
        return MapEntry(key, value);
      }
    });
  }

  void readDeck() {
    state = JsonBackend().readDeckFromJson();
  }

  void _writeDeck() {
    JsonBackend().writeDataToJson(state, 'cards');
  }

  void updateCardTitle(String cardId, String newName) {
    _findAndModifyCardAttribute(
        cardId,
        (oldCard) => LentoCardData(
              cardName: newName,
              blockDuration: oldCard.blockDuration,
              isActivated: oldCard.isActivated,
              blockedItems: oldCard.blockedItems,
              todos: oldCard.todos,
              reminders: oldCard.reminders,
            ));
    _writeDeck();
  }

  void activateCard(String cardId) {
    _findAndModifyCardAttribute(
        cardId,
        (oldCard) => LentoCardData(
              cardName: oldCard.cardName,
              blockDuration: oldCard.blockDuration,
              isActivated: true,
              blockedItems: oldCard.blockedItems,
              todos: oldCard.todos,
              reminders: oldCard.reminders,
            ));
    _writeDeck();
  }

  void deactivateCard(String cardId) {
    _findAndModifyCardAttribute(
        cardId,
        (oldCard) => LentoCardData(
              cardName: oldCard.cardName,
              blockDuration:
                  CardTime.fromPresetTime(oldCard.blockDuration.presetTime),
              isActivated: false,
              blockedItems: oldCard.blockedItems,
              todos: oldCard.todos,
              reminders: oldCard.reminders,
            ));
    _writeDeck();
  }

  void updateCardTime({
    required String cardId,
    required int newValue,
    TimeSection? timeSection,
  }) {
    _findAndModifyCardAttribute(
        cardId,
        (oldCard) => LentoCardData(
              cardName: oldCard.cardName,
              blockDuration: timeSection == null
                  ? CardTime.fromTime(
                      presetTime: oldCard.blockDuration.presetTime,
                      newTime: newValue)
                  : CardTime(
                      presetTime: oldCard.blockDuration.presetTime,
                      hours: timeSection == TimeSection.hours
                          ? newValue
                          : oldCard.blockDuration.hours,
                      minutes: timeSection == TimeSection.minutes
                          ? newValue
                          : oldCard.blockDuration.minutes,
                      seconds: timeSection == TimeSection.seconds
                          ? newValue
                          : oldCard.blockDuration.seconds),
              isActivated: oldCard.isActivated,
              blockedItems: oldCard.blockedItems,
              todos: oldCard.todos,
              reminders: oldCard.reminders,
            ));
    _writeDeck();
  }

  void addNewCard() {
    state = {
      ...state,
      uuID.v4(): LentoCardData.fromDefaults(),
    };
    _writeDeck();
  }

  void removeCard({required String cardId}) {
    state = Map.fromEntries(state.entries.where((e) => e.key != cardId));
    _writeDeck();
  }

  void addBlockedItem({
    required String cardId,
    required BlockedItemData blockedItem,
  }) {
    _findAndModifyCardAttribute(
        cardId,
        (oldCard) => LentoCardData(
              cardName: oldCard.cardName,
              blockDuration: oldCard.blockDuration,
              isActivated: oldCard.isActivated,
              blockedItems: {...oldCard.blockedItems, uuID.v4(): blockedItem},
              todos: oldCard.todos,
              reminders: oldCard.reminders,
            ));
    _writeDeck();
  }

  void deleteBlockItem({
    required String cardId,
    required String blockItemId,
  }) {
    _findAndModifyCardAttribute(
        cardId,
        (oldCard) => LentoCardData(
              cardName: oldCard.cardName,
              blockDuration: oldCard.blockDuration,
              isActivated: oldCard.isActivated,
              blockedItems: Map.from(oldCard.blockedItems)
                ..removeWhere((key, value) => key == blockItemId),
              todos: oldCard.todos,
              reminders: oldCard.reminders,
            ));
    _writeDeck();
  }

  void updateBlockedItem({
    required String cardId,
    required String blockItemId,
    required BlockedItemData newData,
  }) {
    _findAndModifyCardAttribute(
        cardId,
        (oldCard) => LentoCardData(
              cardName: oldCard.cardName,
              blockDuration: oldCard.blockDuration,
              isActivated: oldCard.isActivated,
              blockedItems: Map.fromEntries(oldCard.blockedItems.entries.map(
                  (e) => e.key == blockItemId
                      ? MapEntry(blockItemId, newData)
                      : e)),
              todos: oldCard.todos,
              reminders: oldCard.reminders,
            ));
    _writeDeck();
  }

  void toggleRestrictedAccess({
    required String cardId,
    required String blockItemId,
  }) {
    _findAndModifyCardAttribute(
        cardId,
        (oldCard) => LentoCardData(
              cardName: oldCard.cardName,
              blockDuration: oldCard.blockDuration,
              isActivated: oldCard.isActivated,
              todos: oldCard.todos,
              blockedItems: Map.fromEntries(
                  oldCard.blockedItems.entries.map((e) => e.key == blockItemId
                      ? MapEntry(
                          blockItemId,
                          switch (e.value.type) {
                            BlockItemType.app => BlockedItemData.fromApp(
                                appName: e.value.appName,
                                sourcePaths: e.value.sourcePaths,
                                isEnabled: e.value.isEnabled,
                                isRestrictedAccess: e.key == blockItemId
                                    ? !e.value.isRestrictedAccess
                                    : e.value.isRestrictedAccess,
                                customPopupId: e.value.customPopupId,
                              ),
                            BlockItemType.website => BlockedItemData.fromSite(
                                siteUrl: e.value.siteUrl,
                                isEnabled: e.value.isEnabled,
                                isRestrictedAccess: e.key == blockItemId
                                    ? !e.value.isRestrictedAccess
                                    : e.value.isRestrictedAccess,
                                customPopupId: e.value.customPopupId,
                              )
                          })
                      : e)),
              reminders: oldCard.reminders,
            ));
    _writeDeck();
  }

  void toggleEnabled({
    required String cardId,
    required String blockItemId,
  }) {
    _findAndModifyCardAttribute(
        cardId,
        (oldCard) => LentoCardData(
              cardName: oldCard.cardName,
              blockDuration: oldCard.blockDuration,
              isActivated: oldCard.isActivated,
              todos: oldCard.todos,
              blockedItems: Map.fromEntries(
                  oldCard.blockedItems.entries.map((e) => e.key == blockItemId
                      ? MapEntry(
                          blockItemId,
                          switch (e.value.type) {
                            BlockItemType.app => BlockedItemData.fromApp(
                                appName: e.value.appName,
                                sourcePaths: e.value.sourcePaths,
                                isEnabled: e.key == blockItemId
                                    ? !e.value.isEnabled
                                    : e.value.isEnabled,
                                isRestrictedAccess: e.value.isRestrictedAccess,
                                customPopupId: e.value.customPopupId,
                              ),
                            BlockItemType.website => BlockedItemData.fromSite(
                                siteUrl: e.value.siteUrl,
                                isEnabled: e.key == blockItemId
                                    ? !e.value.isEnabled
                                    : e.value.isEnabled,
                                isRestrictedAccess: e.value.isRestrictedAccess,
                                customPopupId: e.value.customPopupId,
                              )
                          })
                      : e)),
              reminders: oldCard.reminders,
            ));
    _writeDeck();
  }

  void addTodo({
    required String cardId,
    required String title,
    required int timeAllocation,
  }) {
    _findAndModifyCardAttribute(
        cardId,
        (oldCard) => LentoCardData(
              cardName: oldCard.cardName,
              blockDuration: oldCard.blockDuration,
              isActivated: oldCard.isActivated,
              blockedItems: oldCard.blockedItems,
              todos: {
                ...oldCard.todos,
                uuID.v4(): LentoTodo(
                  title: title,
                  completed: false,
                  timeAllocation: timeAllocation,
                ),
              },
              reminders: oldCard.reminders,
            ));
    _writeDeck();
  }

  void toggleTodoCompletion({
    required String cardId,
    required String todoId,
    required int timeAllocation,
  }) {
    _findAndModifyCardAttribute(
        cardId,
        (oldCard) => LentoCardData(
              cardName: oldCard.cardName,
              blockDuration: oldCard.blockDuration,
              isActivated: oldCard.isActivated,
              blockedItems: oldCard.blockedItems,
              todos: oldCard.todos.map((key, value) => key == todoId
                  ? MapEntry(
                      key,
                      LentoTodo(
                        title: value.title,
                        completed: !value.completed,
                        timeAllocation: timeAllocation,
                      ))
                  : MapEntry(key, value)),
              reminders: oldCard.reminders,
            ));
    _writeDeck();
  }

  void deleteTodo({
    required String cardId,
    required String todoId,
  }) {
    _findAndModifyCardAttribute(
        cardId,
        (oldCard) => LentoCardData(
              cardName: oldCard.cardName,
              blockDuration: oldCard.blockDuration,
              isActivated: oldCard.isActivated,
              blockedItems: oldCard.blockedItems,
              todos: Map.fromEntries(
                oldCard.todos.entries.where((e) => e.key != todoId),
              ),
              reminders: oldCard.reminders,
            ));
    _writeDeck();
  }
}

/// Immutable data class for a Lento card.
class LentoCardData extends PretDataclass {
  final String cardName;
  final CardTime blockDuration;
  final bool isActivated;
  final Map<String, LentoTodo> todos;
  final Map<String, BlockedItemData> blockedItems;
  final Map<String, ReminderData> reminders;

  LentoCardData({
    required this.cardName,
    required this.blockDuration,
    required this.isActivated,
    required this.blockedItems,
    required this.todos,
    required this.reminders,
  });

  LentoCardData.fromDefaults()
      : cardName = 'Untitled Card',
        blockDuration = const CardTime.fromPresetTime(0),
        isActivated = false,
        blockedItems = const {},
        todos = const {},
        reminders = const {};

  @override
  Map<String, dynamic> toJson() {
    return {
      'name': cardName,
      'blockDuration': blockDuration.presetTime,
      'isActivated': isActivated,
      'todos': todos.map((key, value) => MapEntry(key, value.toJson())),
      'blockedItems': blockedItems.map((key, value) => MapEntry(
            key,
            value.toJson(),
          )),
      'reminders': reminders.map((key, value) => MapEntry(
            key,
            value.toJson(),
          )),
    };
  }
}

@immutable
class CardTime {
  final int presetTime;
  final int hours;
  final int minutes;
  final int seconds;

  const CardTime(
      {required this.presetTime,
      required this.hours,
      required this.minutes,
      required this.seconds});

  const CardTime.fromPresetTime(this.presetTime)
      : hours = presetTime ~/ 3600,
        minutes = (presetTime % 3600) ~/ 60,
        seconds = presetTime % 60;

  const CardTime.fromTime({required this.presetTime, required newTime})
      : hours = newTime ~/ 3600,
        minutes = (newTime % 3600) ~/ 60,
        seconds = newTime % 60;

  String get fmtHours => hours.toString().padLeft(2, '0');
  String get fmtMinutes => minutes.toString().padLeft(2, '0');
  String get fmtSeconds => seconds.toString().padLeft(2, '0');

  int get gatheredSeconds => hours * 60 * 60 + minutes * 60 + seconds;
}

// I tried to consolidate the common fields in
// these two data classes into a single BlockedItemData
// class that they could extend, but there ended up
// being enough duplication in the constructors that I
// just gave up on it. Maybe there's a better way to do it?
// Return to this later.

class BlockedItemData extends PretDataclass {
  final BlockItemType type;

  final Uri? siteUrl;
  final String? appName;
  final Map<String, String>? sourcePaths;

  final bool isEnabled;
  final bool isRestrictedAccess;
  final String? customPopupId;

  BlockedItemData.newBlockedSite({
    required this.siteUrl,
    this.isRestrictedAccess = false,
    this.customPopupId,
  })  : type = BlockItemType.website,
        isEnabled = true,
        appName = null,
        sourcePaths = null;

  BlockedItemData.newBlockedApp({
    required this.appName,
    required this.sourcePaths,
    this.isRestrictedAccess = false,
    this.customPopupId,
  })  : type = BlockItemType.app,
        siteUrl = null,
        isEnabled = true;

  BlockedItemData.fromSite({
    required this.siteUrl,
    required this.isEnabled,
    required this.isRestrictedAccess,
    required this.customPopupId,
  })  : type = BlockItemType.website,
        appName = null,
        sourcePaths = null;

  BlockedItemData.fromApp({
    required this.appName,
    required this.sourcePaths,
    required this.isEnabled,
    required this.isRestrictedAccess,
    required this.customPopupId,
  })  : type = BlockItemType.app,
        siteUrl = null;

  String? get currentSourcePath => type != BlockItemType.app
      ? throw ArgumentError('Cannot get source path for non-app blockitem!')
      : sourcePaths![Platform.operatingSystem];

  @override
  Map<String, dynamic> toJson() {
    final res = {
      'type': type.toString(),
      'isEnabled': isEnabled,
      'isRestrictedAccess': isRestrictedAccess,
      'customPopupId': customPopupId,
    };
    switch (type) {
      case BlockItemType.app:
        res['appName'] = appName;
        res['sourcePaths'] = sourcePaths;
        break;
      case BlockItemType.website:
        res['siteUrl'] = siteUrl.toString();
    }
    return res;
  }
}

class LentoTodo extends PretDataclass {
  final String title;
  final bool completed;
  final int timeAllocation;

  LentoTodo({
    required this.title,
    required this.completed,
    required this.timeAllocation,
  });

  @override
  Map<String, dynamic> toJson() => {
        'title': title,
        'completed': completed,
        'timeAllocation': timeAllocation,
      };
}

class ReminderData extends PretDataclass {
  final String title;
  final String message;
  final List<String> triggerTimes;

  ReminderData({
    required this.title,
    required this.message,
    required this.triggerTimes,
  });

  @override
  Map<String, dynamic> toJson() => {
        'title': title,
        'message': message,
        'triggerTimes': triggerTimes,
      };
}
