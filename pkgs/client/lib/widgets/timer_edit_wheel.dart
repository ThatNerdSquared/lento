import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../config.dart';
import '../main.dart';

class TimerEditWheel extends ConsumerWidget {
  final String cardId;
  final TimeSection timeSection;
  final Function(String, TimeSection) handleChange;

  const TimerEditWheel({
    super.key,
    required this.cardId,
    required this.timeSection,
    required this.handleChange,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final blockDuration = ref
        .watch(lentoDeckProvider.select((deck) => deck[cardId]!.blockDuration));
    return Column(mainAxisAlignment: MainAxisAlignment.center, children: [
      Text(switch (timeSection) {
        TimeSection.hours => 'Hours',
        TimeSection.minutes => 'Minutes',
        TimeSection.seconds => 'Seconds'
      }),
      TextFormField(
          initialValue: switch (timeSection) {
            TimeSection.hours => blockDuration.hours,
            TimeSection.minutes => blockDuration.minutes,
            TimeSection.seconds => blockDuration.seconds,
          }
              .toString(),
          validator: (val) {
            if (val == null || val.isEmpty || int.tryParse(val) == null) {
              return 'Please enter a valid number!';
            }
            if (0 > int.parse(val) ||
                int.parse(val) > (timeSection == TimeSection.hours ? 23 : 59)) {
              return 'Number is out of range! Please pick a number between 0 and 59, or 0 and 23 for hours.';
            }
            return null;
          },
          keyboardType: TextInputType.number,
          onChanged: (value) => handleChange(value, timeSection))
    ]);
  }
}
