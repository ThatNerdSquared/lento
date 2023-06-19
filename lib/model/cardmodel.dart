import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:uuid/uuid.dart';

/// Class that controls a list of [LentoCardData].
class LentoDeck extends StateNotifier<Map<String, LentoCardData>> {
  LentoDeck({Map<String, LentoCardData>? initialDeck})
      : super(initialDeck ?? <String, LentoCardData>{});

  void _findAndModifyCardAttribute(
      String cardId, Function(LentoCardData oldCard) modifierCallback) {
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
            time: oldCard.time,
            isActivated: oldCard.isActivated,
            blockedSites: oldCard.blockedSites));
  }

  void activateCard(String cardId) {
    _findAndModifyCardAttribute(
        cardId,
        (oldCard) => LentoCardData(
            cardName: oldCard.cardName,
            time: oldCard.time,
            isActivated: true,
            blockedSites: oldCard.blockedSites));
  }

  void deactivateCard(String cardId) {
    _findAndModifyCardAttribute(
        cardId,
        (oldCard) => LentoCardData(
            cardName: oldCard.cardName,
            time: oldCard.time,
            isActivated: false,
            blockedSites: oldCard.blockedSites));
  }
}

/// Immutable data class for a Lento card.
@immutable
class LentoCardData {
  final String cardName;
  final int time;
  final bool isActivated;
  final List<BlockedWebsiteData> blockedSites;

  const LentoCardData(
      {this.cardName = 'Untitled Card',
      this.time = 0,
      this.isActivated = false,
      this.blockedSites = const []});
}

class BlockedWebsiteData {
  Uuid itemId = const Uuid();
  // Uuid itemId;
  // Uri siteUrl = Uri(scheme: 'https', host: 'nathanyeung.ca');
  // bool isAccessRestricted;
  // File iconPath;
  // Uuid? associatedPopup;

  // BlockedWebsiteModel({
  //   this.cardId = const Uuid(),
  //   this.siteUrl ,
  //   this.isAccessRestricted = false,
  //   required this.iconPath = File(''),

  // });
}
