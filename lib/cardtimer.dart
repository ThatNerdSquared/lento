import 'dart:async';

import 'package:flutter/material.dart';
import 'package:numberpicker/numberpicker.dart';

import 'config.dart';

class CardTimer extends StatefulWidget {
  const CardTimer({super.key, required this.startingColour});

  final Color startingColour;

  @override
  State<CardTimer> createState() => _CardTimerState();
}

class _CardTimerState extends State<CardTimer> {
  int _seconds = 0;
  int _minutes = 0;
  int _hours = 0;

  bool _isBlockRunning = false;
  bool _isEditingTimer = false;
  late Color _timerColor = widget.startingColour;

  double _containerWidth = 280.0;
  double _containerHeight = 100.0;

  @override
  Widget build(BuildContext context) {
    return Column(children: [
      MouseRegion(
          onHover: (pointer) {
            setState(() {
              _isBlockRunning
                  ? null
                  : _timerColor = Theme.of(context).colorScheme.surfaceTint;
            });
          },
          onExit: (pointer) {
            setState(() {
              _timerColor = Theme.of(context).colorScheme.surface;

              _containerWidth = 280.0;
              _containerHeight = 100.0;
              _isEditingTimer = false;
            });
          },
          child: GestureDetector(
              onTap: () {
                setState(() {
                  if (!_isBlockRunning) {
                    _containerWidth = 300.0;
                    _containerHeight = 180.0;
                    _isEditingTimer = true;
                  }
                });
              },
              child: Container(
                width: _containerWidth,
                height: _containerHeight,
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
              onPressed: _isBlockRunning ? null : _startTimer,
              style: ElevatedButton.styleFrom(
                  foregroundColor: Theme.of(context).colorScheme.primary,
                  backgroundColor: Theme.of(context).colorScheme.tertiary),
              child: Text(_isBlockRunning ? 'Session Started' : 'Start Block')))
    ]);
  }

  void _startTimer() {
    var presetHours = _hours;
    var presetMinutes = _minutes;
    var presetSeconds = _seconds;
    print(presetHours); // ignore: avoid_print
    print(presetMinutes); //ignore: avoid_print
    print(presetSeconds); //ignore: avoid_print
    setState(() {
      _isBlockRunning = true;
    });

    Timer.periodic(const Duration(seconds: 1), (timer) {
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

      if (_seconds == 0 && _minutes == 0 && _hours == 0) {
        timer.cancel();
        setState(() {
          _isBlockRunning = false;
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
