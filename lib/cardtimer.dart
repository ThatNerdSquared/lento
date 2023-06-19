import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:numberpicker/numberpicker.dart';

import 'config.dart';
import 'main.dart';

class CardTimer extends ConsumerStatefulWidget {
  const CardTimer(
      {super.key, required this.cardId, required this.startingColour});

  final String cardId;
  final Color startingColour;

  @override
  CardTimerState createState() => CardTimerState();
}

class CardTimerState extends ConsumerState<CardTimer> {
  int _seconds = 0;
  int _minutes = 0;
  int _hours = 0;

  bool _isEditingTimer = false;
  late Color _timerColor = widget.startingColour;

  @override
  Widget build(BuildContext context) {
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
                    color: _timerColor,
                    borderRadius: Config.defaultBorderRadius),
                child:
                    Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                  Visibility(
                      visible: !_isEditingTimer,
                      child: Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Text(
                              _formatTime(_hours),
                              style: const TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 40,
                              ),
                            ),
                            const Text(
                              ':',
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 40,
                              ),
                            ),
                            Text(
                              _formatTime(_minutes),
                              style: const TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 40,
                              ),
                            ),
                            const Text(
                              ':',
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 40,
                              ),
                            ),
                            Text(
                              _formatTime(_seconds),
                              style: const TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 40,
                              ),
                            ),
                          ])),
                  Visibility(
                    visible: _isEditingTimer,
                    child: Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                const Text('Hours'),
                                NumberPicker(
                                  value: _hours,
                                  minValue: 0,
                                  maxValue: 23,
                                  onChanged: (value) =>
                                      setState(() => _hours = value),
                                )
                              ]),
                          Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                const Text('Minutes'),
                                NumberPicker(
                                  value: _minutes,
                                  minValue: 0,
                                  maxValue: 59,
                                  onChanged: (value) =>
                                      setState(() => _minutes = value),
                                )
                              ]),
                          Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                const Text('Seconds'),
                                NumberPicker(
                                  value: _seconds,
                                  minValue: 0,
                                  maxValue: 59,
                                  onChanged: (value) =>
                                      setState(() => _seconds = value),
                                )
                              ]),
                        ]),
                  ),
                ]),
              ))),
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
    var presetHours = _hours;
    var presetMinutes = _minutes;
    var presetSeconds = _seconds;
    print(presetHours); // ignore: avoid_print
    print(presetMinutes); //ignore: avoid_print
    print(presetSeconds); //ignore: avoid_print
    ref.read(lentoDeckProvider.notifier).activateCard(widget.cardId);

    Timer.periodic(const Duration(seconds: 1), (timer) {
      if (mounted) {
        setState(() {
          _isEditingTimer = false;
          if (_seconds > 0) {
            _seconds--;
          }
          if (_seconds == 0 && _minutes > 0) {
            _minutes--;
            _seconds = 59;
          }

          if (_minutes == 0 && _hours > 0) {
            _hours--;
            _minutes = 59;
          }
        });
      }

      if (_seconds == 0 && _minutes == 0 && _hours == 0) {
        timer.cancel();
        ref.read(lentoDeckProvider.notifier).deactivateCard(widget.cardId);
        setState(() {
          _seconds = presetSeconds;
          _minutes = presetMinutes;
          _hours = presetHours;
        });
        print('timer complete'); // ignore: avoid_print
      }
    });
  }

  String _formatTime(time) {
    var timeStr = time.toString();
    return timeStr.length == 1 ? '0$timeStr' : timeStr;
  }
}
