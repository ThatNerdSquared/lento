import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../config.dart';
import '../main.dart';
import 'timer_edit_wheel.dart';

class CardTimer extends ConsumerStatefulWidget {
  final String cardId;
  final Color startingColour;

  const CardTimer({
    super.key,
    required this.cardId,
    required this.startingColour,
  });

  @override
  CardTimerState createState() => CardTimerState();
}

class CardTimerState extends ConsumerState<CardTimer> {
  bool _isEditingTimer = false;
  late Color _timerColor = widget.startingColour;

  double _calculateTimerMargin(maxWidth, isEditingTimer) {
    if (isEditingTimer &&
        ((maxWidth * 2 * Config.defaultMarginPercentage) < 300)) {
      return 0.05 * maxWidth;
    } else {
      return Config.defaultMarginPercentage * maxWidth;
    }
  }

  @override
  Widget build(BuildContext context) {
    var blockDuration = ref.watch(
        lentoDeckProvider.select((deck) => deck[widget.cardId]!.blockDuration));
    var isCardActivated =
        ref.watch(lentoDeckProvider)[widget.cardId]!.isActivated;

    return LayoutBuilder(
      builder: (context, constraints) => Column(children: [
        MouseRegion(
          onHover: (pointer) {
            setState(() {
              isCardActivated
                  ? null
                  : _timerColor = Theme.of(context).colorScheme.surfaceTint;
            });
          },
          onExit: (pointer) {
            setState(() {
              _timerColor = Theme.of(context).colorScheme.surface;
              _isEditingTimer = false;
            });
          },
          child: GestureDetector(
            onTap: () {
              setState(() {
                if (!isCardActivated) {
                  _isEditingTimer = true;
                }
              });
            },
            child: Container(
              margin: EdgeInsets.only(
                left: _calculateTimerMargin(
                    constraints.maxWidth, _isEditingTimer),
                right: _calculateTimerMargin(
                    constraints.maxWidth, _isEditingTimer),
              ),
              padding: const EdgeInsets.only(
                top: Config.defaultElementSpacing * 3 / 2,
                bottom: Config.defaultElementSpacing * 3 / 2,
              ),
              decoration: BoxDecoration(
                color: _timerColor,
                borderRadius: Config.defaultBorderRadius,
              ),
              child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: !_isEditingTimer
                      ? [
                          for (final item in [
                            blockDuration.fmtHours,
                            ':',
                            blockDuration.fmtMinutes,
                            ':',
                            blockDuration.fmtSeconds
                          ])
                            Text(
                              item,
                              style: const TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 40,
                              ),
                            )
                        ]
                      : [
                          for (final timeSection in TimeSection.values)
                            TimerEditWheel(
                              cardId: widget.cardId,
                              timeSection: timeSection,
                            )
                        ]),
            ),
          ),
        ),
        const Padding(
            padding: EdgeInsets.all(Config.defaultElementSpacing * 1 / 2)),
        Container(
            decoration: const BoxDecoration(
                borderRadius: Config.defaultBorderRadius,
                boxShadow: [Config.defaultShadow]),
            child: ElevatedButton(
                onPressed: isCardActivated ? null : _startTimer,
                style: ElevatedButton.styleFrom(
                    foregroundColor: Theme.of(context).colorScheme.primary,
                    backgroundColor: Theme.of(context).colorScheme.tertiary),
                child:
                    Text(isCardActivated ? 'Session Started' : 'Start Block')))
      ]),
    );
  }

  void _startTimer() {
    ref.read(lentoDeckProvider.notifier).activateCard(widget.cardId);

    Timer.periodic(const Duration(seconds: 1), (timer) {
      if (mounted) {
        var blockDuration = ref.read(lentoDeckProvider
            .select((deck) => deck[widget.cardId]!.blockDuration));
        var newDuration = blockDuration.gatheredSeconds - 1;
        ref.read(lentoDeckProvider.notifier).updateCardTime(
              cardId: widget.cardId,
              newValue: newDuration,
            );

        if (newDuration == 0) {
          timer.cancel();
          ref.read(lentoDeckProvider.notifier).deactivateCard(widget.cardId);
          print('timer complete'); // ignore: avoid_print
        }
      }
    });
  }
}
