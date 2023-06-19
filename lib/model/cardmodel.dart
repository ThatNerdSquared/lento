import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:uuid/uuid.dart';

/// Class that controls a list of [LentoCardData].
class LentoDeck extends StateNotifier<Map<String, LentoCardData>> {
  LentoDeck({Map<String, LentoCardData>? initialDeck})
      : super(initialDeck ?? <String, LentoCardData>{});

  void updateCardTitle(String cardId, String newName) {
    state = state.map((key, value) {
      if (key == cardId) {
        return MapEntry(
            key,
            LentoCardData(
                cardName: newName,
                time: value.time,
                blockedSites: value.blockedSites));
      } else {
        return MapEntry(key, value);
      }
    });
  }
}

/// Immutable data class for a Lento card.
@immutable
class LentoCardData {
  final String cardName;
  final int time;
  final List<BlockedWebsiteData> blockedSites;

  const LentoCardData(
      {this.cardName = 'Untitled Card',
      this.time = 0,
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
