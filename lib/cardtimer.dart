import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'config.dart';
import 'main.dart';
import 'widgets/timer_edit_wheel.dart';

class CardTime {
  late int hours;
  late int minutes;
  late int seconds;

  CardTime({required presetTime}) {
    hours = presetTime ~/ 3600;
    minutes = (presetTime % 3600) ~/ 60;
    seconds = presetTime % 60;
  }

  String get fmtHours => hours.toString().padLeft(2, '0');
  String get fmtMinutes => minutes.toString().padLeft(2, '0');
  String get fmtSeconds => seconds.toString().padLeft(2, '0');

  int get gatheredSeconds => hours * 60 * 60 + minutes * 60 + seconds;
}

class CardTimer extends ConsumerStatefulWidget {
  const CardTimer(
      {super.key, required this.cardId, required this.startingColour});

  final String cardId;
  final Color startingColour;

  @override
  CardTimerState createState() => CardTimerState();
}

class CardTimerState extends ConsumerState<CardTimer> {
  bool _isEditingTimer = false;
  late Color _timerColor = widget.startingColour;
  late CardTime cardTime;

  @override
  Widget build(BuildContext context) {
    setState(() {
      cardTime = CardTime(
          presetTime: ref.watch(lentoDeckProvider
              .select((deck) => deck[widget.cardId]!.blockDuration)));
    });

    var isCardActivated =
        ref.watch(lentoDeckProvider)[widget.cardId]!.isActivated;

    return Column(children: [
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
            width: _isEditingTimer ? 300.0 : 280.0,
            height: _isEditingTimer ? 180.0 : 100.0,
            padding: EdgeInsets.zero,
            decoration: BoxDecoration(
                color: _timerColor, borderRadius: Config.defaultBorderRadius),
            child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: !_isEditingTimer
                    ? [
                        for (final item in [
                          cardTime.fmtHours,
                          ':',
                          cardTime.fmtMinutes,
                          ':',
                          cardTime.fmtSeconds
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
                        TimerEditWheel(
                            cardId: widget.cardId,
                            timeSection: TimeSection.hours,
                            value: cardTime.hours,
                            stateUpdateCallback: (value) =>
                                cardTime.hours = value,
                            gatheredSecondsGetter: () =>
                                cardTime.gatheredSeconds),
                        TimerEditWheel(
                            cardId: widget.cardId,
                            timeSection: TimeSection.minutes,
                            value: cardTime.minutes,
                            stateUpdateCallback: (value) =>
                                cardTime.minutes = value,
                            gatheredSecondsGetter: () =>
                                cardTime.gatheredSeconds),
                        TimerEditWheel(
                            cardId: widget.cardId,
                            timeSection: TimeSection.seconds,
                            value: cardTime.seconds,
                            stateUpdateCallback: (value) =>
                                cardTime.seconds = value,
                            gatheredSecondsGetter: () =>
                                cardTime.gatheredSeconds),
                      ]),
          ),
        ),
      ),
      const Padding(
          padding:
              EdgeInsets.only(bottom: Config.defaultElementSpacing * 2 / 3)),
      Container(
          decoration: const BoxDecoration(
              borderRadius: Config.defaultBorderRadius,
              boxShadow: [Config.defaultShadow]),
          child: ElevatedButton(
              onPressed: isCardActivated ? null : _startTimer,
              style: ElevatedButton.styleFrom(
                  foregroundColor: Theme.of(context).colorScheme.primary,
                  backgroundColor: Theme.of(context).colorScheme.tertiary),
              child: Text(isCardActivated ? 'Session Started' : 'Start Block')))
    ]);
  }

  void _startTimer() {
    // var presetHours = _hours;
    // var presetMinutes = _minutes;
    // var presetSeconds = _seconds;
    // print(presetHours); // ignore: avoid_print
    // print(presetMinutes); //ignore: avoid_print
    // print(presetSeconds); //ignore: avoid_print
    // ref.read(lentoDeckProvider.notifier).activateCard(widget.cardId);

    // Timer.periodic(const Duration(seconds: 1), (timer) {
    //   if (mounted) {
    //     setState(() {
    //       _isEditingTimer = false;
    //       if (_seconds > 0) {
    //         _seconds--;
    //       }
    //       if (_seconds == 0 && _minutes > 0) {
    //         _minutes--;
    //         _seconds = 59;
    //       }

    //       if (_minutes == 0 && _hours > 0) {
    //         _hours--;
    //         _minutes = 59;
    //       }
    //     });
    //   }

    //   if (_seconds == 0 && _minutes == 0 && _hours == 0) {
    //     timer.cancel();
    //     ref.read(lentoDeckProvider.notifier).deactivateCard(widget.cardId);
    //     setState(() {
    //       _seconds = presetSeconds;
    //       _minutes = presetMinutes;
    //       _hours = presetHours;
    //     });
    //     print('timer complete'); // ignore: avoid_print
    //   }
    // });
  }
}