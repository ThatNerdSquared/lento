import 'package:flutter/material.dart';
import 'package:numberpicker/numberpicker.dart';
import 'dart:async';

class cardTimer extends StatefulWidget{
  const cardTimer({super.key});

  @override
  State<cardTimer> createState() => _cardTimerState();
  
}


class _cardTimerState extends State<cardTimer> {
  int _seconds = 0;
  int _minutes = 0;
  int _hours = 0;
  int _currentValue = 3;

  late String _secondsString = "0" + _seconds.toString();
  late String _minutesString = "0" + _minutes.toString();
  late String _hoursString = "0" + _hours.toString();

  bool _displayVisible = true;
  bool _editVisible = false;
  bool _buttonVisible = false;
  bool _isDisabled = false;

  var _editIcon = Icon(Icons.edit_note);
  var _timerColor = Colors.grey[200];
  var _timerPadding = EdgeInsets.zero;

  double _containerWidth = 280.0;
  double _containerHeight = 100.0;

  var _buttonText =  Text("Start");
  var _buttonStyle = ElevatedButton.styleFrom(
              foregroundColor: Colors.white as Color,
              backgroundColor: const Color(0xFF85b718)
            );

  Timer? _timer;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        MouseRegion(
          onHover: (PointerEvent pointer){
            setState((){
              _timerColor = Color(0xFFeef2ef);
            });
          },
          onExit: (PointerEvent pointer){
            setState((){
              _timerColor = Colors.grey[200];              _displayVisible = true;
              _editVisible = false;
              _secondsString = _seconds.toString();
              _minutesString = _minutes.toString();
              _hoursString = _hours.toString();

              if(_secondsString.length == 1){
                _secondsString = "0" + _secondsString;
              }

              if (_minutesString.length == 1){
                _minutesString = "0" + _minutesString;
              }

              if (_hoursString.length == 1){
                _hoursString = "0" + _hoursString;
              }
              _buttonVisible = false;

              _timerPadding = EdgeInsets.zero;
              _containerWidth = 280.0;
              _containerHeight = 100.0;

            }
            );
          },

          child:
              GestureDetector(
                onTap: (){
                  setState(() {
                  _containerWidth = 300.0;
                  _containerHeight = 180.0;
                  _editVisible = true;
                  _displayVisible = false;
                });
                },
                child:
                  Container(
                    width: _containerWidth,
                    height: _containerHeight,
                    padding: _timerPadding,
                    decoration: BoxDecoration(
                      color: _timerColor,
                      borderRadius: BorderRadius.all(Radius.circular(10))
                    ),

                    child:
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                            Visibility(
                              visible: _displayVisible,
                              child:
                              Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Text(
                                      _hoursString,
                                      style: TextStyle(
                                        fontWeight: FontWeight.bold,
                                        fontSize: 40,
                                      ),
                                    ),

                                  Text(
                                    ":",
                                    style: TextStyle(
                                          fontWeight: FontWeight.bold,
                                          fontSize: 40,
                                        ),
                                  ),

                                  Text(
                                      _minutesString,
                                      style: TextStyle(
                                        fontWeight: FontWeight.bold,
                                        fontSize: 40,
                                      ),
                                    ),

                                  Text(
                                    ":",
                                    style: TextStyle(
                                          fontWeight: FontWeight.bold,
                                          fontSize: 40,
                                        ),
                                  ),

                                    Text(
                                      _secondsString,
                                      style: TextStyle(
                                        fontWeight: FontWeight.bold,
                                        fontSize: 40,
                                      ),
                                    ),
                                ]
                            )
                          ),

                          Visibility(
                            visible: _editVisible,
                            child: 
                              Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Column(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      Text(
                                        "Hours"
                                      ),
                                      NumberPicker(
                                        value: _hours,
                                        minValue: 0,
                                        maxValue: 99,
                                        onChanged: (value) => setState(() => _hours = value),
                                      )
                                    ]
                                  ),
                                  Column(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      Text(
                                        "Minutes"
                                      ),
                                      NumberPicker(
                                        value: _minutes,
                                        minValue: 0,
                                        maxValue: 99,
                                        onChanged: (value) => setState(() => _minutes = value),
                                      )
                                    ]
                                  ),
                                  Column(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      Text(
                                        "Seconds"
                                      ),
                                      NumberPicker(
                                        value: _seconds,
                                        minValue: 0,
                                        maxValue: 99,
                                        onChanged: (value) => setState(() => _seconds = value),
                                      )
                                    ]
                                  ),
                                ]
                              ),
                          ),
                        ]
                      ),
                  ) 
              )
            ),

          Padding(
            padding: const EdgeInsets.only(bottom: 10.0)
          ),

          ElevatedButton(
            onPressed: _isDisabled? null : () => _startTimer(),
            child: _buttonText,
            style: _buttonStyle
          )
        ]
      );
  }

  void _startTimer() {
    int _presetHours = _hours;
    int _presetMinutes = _minutes;
    int _presetSeconds = _seconds;
    print(_presetHours);
    print(_presetMinutes);
    print(_presetSeconds);

    _timer = Timer.periodic(const Duration(seconds: 1), (timer) {
      setState(() {
        _isDisabled = true;
        _editVisible = false;
        _buttonVisible = false;
        _buttonText =  Text("Session Started");

        if (_seconds > 0) {
          _seconds-- ;
          _secondsString = timeString(_seconds);
        } 
        if(_seconds == 0 && _minutes > 0 ) {
          _minutes-- ;
          _minutesString = timeString(_minutes);
          _seconds = 59;
          _secondsString = _seconds.toString();
        }

        if(_minutes == 0 && _hours > 0){
          _hours-- ;
          _hoursString = timeString(_hours);
          _minutes = 59;
          _minutesString = _minutes.toString();
        }
        });

        if(_seconds == 0 && _minutes == 0 && _hours == 0){
          timer.cancel();
          print("******");
          print(_presetHours);
          print(_presetMinutes);
          print(_presetSeconds);

          _reset(_presetHours, _presetMinutes, _presetSeconds);
        }
        });

  }

void _reset(hours, minutes, seconds){
  setState((){
    _isDisabled = false;
      _buttonText =  Text("Start");
      _buttonStyle = ElevatedButton.styleFrom(
              foregroundColor: Colors.white,
              backgroundColor: const Color(0xFF85b718)
            );
      _hoursString = timeString(hours);
      _minutesString = timeString(minutes);
      _secondsString = timeString(seconds);

      _seconds = seconds;
      _minutes = minutes;
      _hours = hours;
  });
}

String timeString(time){
  String timeStr = time.toString();
  if (timeStr.length == 1){
    timeStr = "0" + timeStr;
  }

  return timeStr;
}
}