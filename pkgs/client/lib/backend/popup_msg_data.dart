import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../main.dart';
import 'json_backend.dart';

class PopupMsgs extends StateNotifier<Map<String, String>> {
  PopupMsgs({Map<String, String>? initialPopupMsgs})
      : super(initialPopupMsgs ?? {}) {
    readPopupMsgs();
  }

  void readPopupMsgs() => state = JsonBackend().readPopupMsgsFromJson();

  void _writePopupMsgs() => JsonBackend().writePopupMsgsToJson(state);

  void addPopup(String customMessage) {
    state = {
      ...state,
      uuID.v4(): customMessage,
    };
    _writePopupMsgs();
  }

  void removePopup({required String popupId}) {
    state = Map.fromEntries(state.entries.where((e) => e.key != popupId));
    _writePopupMsgs();
  }
}
