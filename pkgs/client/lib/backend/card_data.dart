import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

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
    JsonBackend().writeDeckToJson(state);
  }

  void updateCardTitle(String cardId, String newName) {
    _findAndModifyCardAttribute(
        cardId,
        (oldCard) => LentoCardData(
            cardName: newName,
            blockDuration: oldCard.blockDuration,
            isActivated: oldCard.isActivated,
            blockedSites: oldCard.blockedSites));
    _writeDeck();
  }

  void activateCard(String cardId) {
    _findAndModifyCardAttribute(
        cardId,
        (oldCard) => LentoCardData(
            cardName: oldCard.cardName,
            blockDuration: oldCard.blockDuration,
            isActivated: true,
            blockedSites: oldCard.blockedSites));
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
              blockedSites: oldCard.blockedSites,
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
            blockedSites: oldCard.blockedSites));
    _writeDeck();
  }

  void addNewCard() {
    state[uuID.v4()] = const LentoCardData();
    _writeDeck();
  }

  void removeCard({required String cardId}) {
    state.removeWhere((key, value) => key == cardId);
    _writeDeck();
  }

  void addBlockedWebsite({
    required String cardId,
    required BlockedWebsiteData websiteData,
  }) {
    _findAndModifyCardAttribute(
        cardId,
        (oldCard) => LentoCardData(
              cardName: oldCard.cardName,
              blockDuration: oldCard.blockDuration,
              isActivated: oldCard.isActivated,
              blockedSites: {...oldCard.blockedSites, uuID.v4(): websiteData},
              blockedApps: oldCard.blockedApps,
            ));
    _writeDeck();
  }

  void addBlockedApp({
    required String cardId,
    required BlockedAppData appData,
  }) {
    _findAndModifyCardAttribute(
        cardId,
        (oldCard) => LentoCardData(
              cardName: oldCard.cardName,
              blockDuration: oldCard.blockDuration,
              isActivated: oldCard.isActivated,
              blockedSites: oldCard.blockedSites,
              blockedApps: {...oldCard.blockedApps, uuID.v4(): appData},
            ));
    _writeDeck();
  }
}

/// Immutable data class for a Lento card.
@immutable
class LentoCardData {
  final String cardName;
  final CardTime blockDuration;
  final bool isActivated;
  final Map<String, BlockedWebsiteData> blockedSites;
  final Map<String, BlockedAppData> blockedApps;

  const LentoCardData({
    this.cardName = 'Untitled Card',
    this.blockDuration = const CardTime.fromPresetTime(0),
    this.isActivated = false,
    this.blockedSites = const {},
    this.blockedApps = const {},
  });

  Map<String, dynamic> toJson() {
    return {
      'name': cardName,
      'blockDuration': blockDuration.presetTime,
      'isActivated': isActivated,
      'blockedSites': blockedSites.map((key, value) => MapEntry(
            key,
            value.toJson(),
          )),
      'blockedApps': blockedApps.map((key, value) => MapEntry(
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

@immutable
class BlockedWebsiteData {
  final Uri siteUrl;
  final bool isEnabled;
  final bool isRestrictedAccess;
  final String? customPopupId;

  const BlockedWebsiteData({
    required this.siteUrl,
    this.isEnabled = true,
    this.isRestrictedAccess = false,
    this.customPopupId,
  });

  Map<String, dynamic> toJson() {
    return {
      'siteUrl': siteUrl.toString(),
      'isEnabled': isEnabled,
      'isRestrictedAccess': isRestrictedAccess,
      'customPopupId': customPopupId,
    };
  }
}

@immutable
class BlockedAppData {
  final String appName;
  final Map<String, String>? sourcePaths;
  final bool isEnabled;
  final bool isRestrictedAccess;
  final String? customPopupId;

  const BlockedAppData({
    required this.appName,
    required this.sourcePaths,
    this.isEnabled = true,
    this.isRestrictedAccess = false,
    this.customPopupId,
  });

  String? get currentSourcePath => sourcePaths![Platform.operatingSystem];

  Map<String, dynamic> toJson() {
    return {
      'appName': appName,
      'sourcePaths': sourcePaths,
      'isEnabled': isEnabled,
      'isRestrictedAccess': isRestrictedAccess,
      'customPopupId': customPopupId,
    };
  }
}
