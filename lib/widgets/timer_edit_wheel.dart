import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:numberpicker/numberpicker.dart';

import '../config.dart';
import '../main.dart';

class TimerEditWheel extends ConsumerWidget {
  final String cardId;
  final TimeSection timeSection;

  const TimerEditWheel({
    super.key,
    required this.cardId,
    required this.timeSection,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    var blockDuration = ref
        .watch(lentoDeckProvider.select((deck) => deck[cardId]!.blockDuration));
    return Column(mainAxisAlignment: MainAxisAlignment.center, children: [
      Text(switch (timeSection) {
        TimeSection.hours => 'Hours',
        TimeSection.minutes => 'Minutes',
        TimeSection.seconds => 'Seconds'
      }),
      NumberPicker(
        value: switch (timeSection) {
          TimeSection.hours => blockDuration.hours,
          TimeSection.minutes => blockDuration.minutes,
          TimeSection.seconds => blockDuration.seconds,
        },
        minValue: 0,
        maxValue: timeSection == TimeSection.hours ? 23 : 60,
        onChanged: (value) {
          ref
              .read(lentoDeckProvider.notifier)
              .updateCardTime(cardId, timeSection, value);
        },
      )
    ]);
  }
}
