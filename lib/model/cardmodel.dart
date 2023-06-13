import 'package:flutter/material.dart';
import 'package:uuid/uuid.dart';

class LentoDeckModel extends ChangeNotifier {
  Uuid? activatedCard;
  List<LentoCardModel> cards;

  LentoDeckModel({this.activatedCard, required this.cards});
}

class LentoCardModel extends ChangeNotifier {
  Uuid cardId;
  String cardName;
  int time;
  List<BlockedWebsiteModel> blockedSites;

  LentoCardModel(
      {this.cardId = const Uuid(),
      this.cardName = 'Untitled Card',
      this.time = 0,
      this.blockedSites = const []});

  void updateCardTitle(String value) {
    cardName = value;
    print(cardName);
    notifyListeners();
  }
}

class BlockedWebsiteModel extends ChangeNotifier {
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
