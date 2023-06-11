import 'package:flutter/material.dart';
import "cardtitle.dart";
import "cardblocklist.dart";
import "cardtimer.dart";
import "cardtitle.dart";
import "timerexample.dart";

// main lento card

class LentoCard extends StatelessWidget{
  const LentoCard({super.key}); // ?
  @override // ?
  
  
  Widget build(BuildContext context){

    return SizedBox(
        width: 350.0,
        height: 450.0,
        child:
          Container(
            decoration: new BoxDecoration(
            boxShadow: [
                new BoxShadow(
                color: Colors.grey[300] as Color,
                blurRadius: 20.0
                )
            ]
            ),
            child:
              Card(
                color: const Color(0xFFFFFFFF),
                shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(20.0),
                ),
                  child: 
                    Padding(
                      padding: EdgeInsets.only(top: 10.0),
                      child:
                        Column(
                          mainAxisAlignment: MainAxisAlignment.start,
                          children: [
                          cardTitle(),
                          Padding(
                            padding: EdgeInsets.only(bottom: 10.0)
                          ),
                          cardTimer()
                          ]
                        )
                )
              )
            )
          );
  }

}