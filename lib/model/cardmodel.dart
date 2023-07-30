import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../config.dart';
import '../main.dart';

/// Class that controls a list of [LentoCardData].
class LentoDeck extends StateNotifier<Map<String, LentoCardData>> {
  LentoDeck(Map<String, LentoCardData>? initialDeck)
      : super(initialDeck ?? <String, LentoCardData>{});
  

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

  void updateCardTitle(String cardId, String newName) {
    _findAndModifyCardAttribute(
        cardId,
        (oldCard) => LentoCardData(
            cardName: newName,
            blockDuration: oldCard.blockDuration,
            isActivated: oldCard.isActivated,
            blockedSites: oldCard.blockedSites));
  }

  void activateCard(String cardId) {
    _findAndModifyCardAttribute(
        cardId,
        (oldCard) => LentoCardData(
            cardName: oldCard.cardName,
            blockDuration: oldCard.blockDuration,
            isActivated: true,
            blockedSites: oldCard.blockedSites));
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
  }

  void addNewCard() {
    state[uuID.v4()] = const LentoCardData();
  }

  void removeCard({required String cardId}) {
    state.removeWhere((key, value) => key == cardId);
  }
}

/// Immutable data class for a Lento card.
@immutable
class LentoCardData {
  final String cardName;
  final CardTime blockDuration;
  final bool isActivated;
  final List<BlockedWebsiteData> blockedSites;

  const LentoCardData(
      {this.cardName = 'Untitled Card',
      this.blockDuration = const CardTime.fromPresetTime(0),
      this.isActivated = false,
      this.blockedSites = const []});
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

@immutable
class BlockedWebsiteData {
  final String itemId;
  final Uri siteUrl;
  final bool isAccessRestricted;
  final File iconPath;
  final String? associatedPopup;

  const BlockedWebsiteData(
      {required this.itemId,
      required this.siteUrl,
      this.isAccessRestricted = false,
      required this.iconPath,
      this.associatedPopup});
}
