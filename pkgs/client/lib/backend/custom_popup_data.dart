import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../main.dart';

class PopupMsgs extends StateNotifier<Map<String, String>> {
  PopupMsgs({Map<String, String>? initialPopupMsgs})
      : super(initialPopupMsgs ?? {});

  void addPopup(String customMessage) => state[uuID.v4()] = customMessage;

  void removePopup({required String popupId}) => state.removeWhere(
        (key, value) => key == popupId,
      );
}
