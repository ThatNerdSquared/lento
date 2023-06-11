import 'dart:async';

import 'package:flutter/material.dart';
import 'package:numberpicker/numberpicker.dart';

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

  late String _secondsString = '0$_seconds';
  late String _minutesString = '0$_minutes';
  late String _hoursString = '0$_hours';

  bool _displayVisible = true;
  bool _editVisible = false;
  bool _isDisabled = false;

  late Color _timerColor = widget.startingColour;
  var _timerPadding = EdgeInsets.zero;

  double _containerWidth = 280.0;
  double _containerHeight = 100.0;

  var _buttonText = const Text('Start Block');

  @override
  Widget build(BuildContext context) {
    return Column(children: [
      MouseRegion(
          onHover: (pointer) {
            setState(() {
              _timerColor = Theme.of(context).colorScheme.surfaceTint;
            });
          },
          onExit: (pointer) {
            setState(() {
              _timerColor = Theme.of(context).colorScheme.surface;
              _displayVisible = true;
              _editVisible = false;
              _secondsString = _seconds.toString();
              _minutesString = _minutes.toString();
              _hoursString = _hours.toString();

              if (_secondsString.length == 1) {
                _secondsString = '0$_secondsString';
              }

              if (_minutesString.length == 1) {
                _minutesString = '0$_minutesString';
              }

              if (_hoursString.length == 1) {
                _hoursString = '0$_hoursString';
              }

              _timerPadding = EdgeInsets.zero;
              _containerWidth = 280.0;
              _containerHeight = 100.0;
            });
          },
          child: GestureDetector(
              onTap: () {
                setState(() {
                  _containerWidth = 300.0;
                  _containerHeight = 180.0;
                  _editVisible = true;
                  _displayVisible = false;
                });
              },
              child: Container(
                width: _containerWidth,
                height: _containerHeight,
                padding: _timerPadding,
                decoration: BoxDecoration(
                    color: _timerColor,
                    borderRadius: const BorderRadius.all(Radius.circular(10))),
                child:
                    Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                  Visibility(
                      visible: _displayVisible,
                      child: Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Text(
                              _hoursString,
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
                              _minutesString,
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
                              _secondsString,
                              style: const TextStyle(
                                fontWeight: FontWeight.bold,
                                fontSize: 40,
                              ),
                            ),
                          ])),
                  Visibility(
                    visible: _editVisible,
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
                                  maxValue: 99,
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
                                  maxValue: 99,
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
                                  maxValue: 99,
                                  onChanged: (value) =>
                                      setState(() => _seconds = value),
                                )
                              ]),
                        ]),
                  ),
                ]),
              ))),
      const Padding(padding: EdgeInsets.only(bottom: 10.0)),
      ElevatedButton(
          onPressed: _isDisabled ? null : _startTimer,
          style: ElevatedButton.styleFrom(
              foregroundColor: Theme.of(context).colorScheme.primary,
              backgroundColor: Theme.of(context).colorScheme.tertiary),
          child: _buttonText)
    ]);
  }

  void _startTimer() {
    var presetHours = _hours;
    var presetMinutes = _minutes;
    var presetSeconds = _seconds;
    print(presetHours); // ignore: avoid_print
    print(presetMinutes); //ignore: avoid_print
    print(presetSeconds); //ignore: avoid_print

    Timer.periodic(const Duration(seconds: 1), (timer) {
      setState(() {
        _isDisabled = true;
        _editVisible = false;
        _buttonText = const Text('Session Started');

        if (_seconds > 0) {
          _seconds--;
          _secondsString = _timeString(_seconds);
        }
        if (_seconds == 0 && _minutes > 0) {
          _minutes--;
          _minutesString = _timeString(_minutes);
          _seconds = 59;
          _secondsString = _seconds.toString();
        }

        if (_minutes == 0 && _hours > 0) {
          _hours--;
          _hoursString = _timeString(_hours);
          _minutes = 59;
          _minutesString = _minutes.toString();
        }
      });

      if (_seconds == 0 && _minutes == 0 && _hours == 0) {
        timer.cancel();
        print('******'); // ignore: avoid_print
        print(presetHours); // ignore: avoid_print
        print(presetMinutes); // ignore: avoid_print
        print(presetSeconds); // ignore: avoid_print

        _reset(presetHours, presetMinutes, presetSeconds);
      }
    });
  }

  void _reset(hours, minutes, seconds) {
    setState(() {
      _isDisabled = false;
      _buttonText = const Text('Start Block');
      // _buttonStyle = ElevatedButton.styleFrom(
      //     foregroundColor: Colors.white,
      //     backgroundColor: const Color(0xFF85b718));
      _hoursString = _timeString(hours);
      _minutesString = _timeString(minutes);
      _secondsString = _timeString(seconds);

      _seconds = seconds;
      _minutes = minutes;
      _hours = hours;
    });
  }

  String _timeString(time) {
    var timeStr = time.toString();
    if (timeStr.length == 1) {
      timeStr = '0$timeStr';
    }

    return timeStr;
  }
}
