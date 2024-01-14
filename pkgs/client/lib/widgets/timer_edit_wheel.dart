import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:pret_a_porter/pret_a_porter.dart';

import '../config.dart';
import '../main.dart';

class TimerEditWheel extends ConsumerWidget {
  final String cardId;
  final TimeSection timeSection;
  final Function(String, TimeSection) handleChange;
  final double fullTimerWidth;
  final FocusNode? focusNode;

  const TimerEditWheel({
    super.key,
    required this.cardId,
    required this.timeSection,
    required this.handleChange,
    required this.fullTimerWidth,
    this.focusNode,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final blockDuration = ref
        .watch(lentoDeckProvider.select((deck) => deck[cardId]!.blockDuration));
    return LayoutBuilder(builder: (context, constraints) {
      return Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          SizedBox(
            width: fullTimerWidth / 5,
            child: TextFormField(
                focusNode: focusNode,
                decoration: const InputDecoration(
                  isDense: true,
                  counterText: '',
                ),
                initialValue: switch (timeSection) {
                  TimeSection.hours => blockDuration.hours,
                  TimeSection.minutes => blockDuration.minutes,
                  TimeSection.seconds => blockDuration.seconds,
                }
                    .toString(),
                maxLength: 2,
                validator: (val) {
                  if (val == null || val.isEmpty || int.tryParse(val) == null) {
                    return 'Please enter a valid number!';
                  }
                  if (0 > int.parse(val) ||
                      int.parse(val) >
                          (timeSection == TimeSection.hours ? 23 : 59)) {
                    return 'Number is out of range! Please pick a number between 0 and 59, or 0 and 23 for hours.';
                  }
                  return null;
                },
                keyboardType: TextInputType.number,
                onChanged: (value) => handleChange(value, timeSection)),
          ),
          Text(switch (timeSection) {
            TimeSection.hours => 'h',
            TimeSection.minutes => 'm',
            TimeSection.seconds => 's'
          }),
          const Padding(
            padding: EdgeInsets.only(
              right: PretConfig.defaultElementSpacing,
            ),
          )
        ],
      );
    });
  }
}
