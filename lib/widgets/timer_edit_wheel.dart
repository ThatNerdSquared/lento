import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:numberpicker/numberpicker.dart';

import '../config.dart';
import '../main.dart';

class TimerEditWheel extends ConsumerWidget {
  final String cardId;
  final TimeSection timeSection;
  final int value;
  final Function(int value) stateUpdateCallback;
  final Function() gatheredSecondsGetter;

  const TimerEditWheel(
      {super.key,
      required this.cardId,
      required this.timeSection,
      required this.value,
      required this.stateUpdateCallback,
      required this.gatheredSecondsGetter});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Column(mainAxisAlignment: MainAxisAlignment.center, children: [
      Text(switch (timeSection) {
        TimeSection.hours => 'Hours',
        TimeSection.minutes => 'Minutes',
        TimeSection.seconds => 'Seconds'
      }),
      NumberPicker(
        value: value,
        minValue: 0,
        maxValue: timeSection == TimeSection.hours ? 23 : 60,
        onChanged: (newValue) {
          stateUpdateCallback(newValue);
          ref
              .read(lentoDeckProvider.notifier)
              .updateCardTime(cardId, gatheredSecondsGetter());
        },
      )
    ]);
  }
}
