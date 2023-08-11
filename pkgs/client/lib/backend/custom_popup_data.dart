import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../main.dart';

class CustomPopupList extends StateNotifier<Map<String, CustomPopup>> {
  CustomPopupList({Map<String, CustomPopup>? initialPopupList})
      : super(initialPopupList ?? {});

  void addPopup(String customMessage) {
    state[uuID.v4()] = CustomPopup(
      customMessage: customMessage,
    );
  }

  void removePopup({required String popupId}) {
    state.removeWhere((key, value) => key == popupId);
  }
}

@immutable
class CustomPopup {
  final String customMessage;

  const CustomPopup({required this.customMessage});
}
