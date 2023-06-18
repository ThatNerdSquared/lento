import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:uuid/uuid.dart';

/// Class that contorls a list of [LentoCardData].
class LentoDeck extends StateNotifier<List<LentoCardData>> {
  LentoDeck({List<LentoCardData>? initialDeck}) : super(initialDeck ?? []);

  void updateCardTitle(String cardId, String newName) {
    state = [
      for (final card in state)
        if (card.cardId == cardId)
          LentoCardData(
              cardId: cardId,
              cardName: newName,
              time: card.time,
              blockedSites: card.blockedSites)
        else
          card
    ];
  }
}

/// Immutable data class for a Lento card.
@immutable
class LentoCardData {
  final String cardId;
  final String cardName;
  final int time;
  final List<BlockedWebsiteData> blockedSites;

  const LentoCardData(
      {required this.cardId,
      this.cardName = 'Untitled Card',
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
