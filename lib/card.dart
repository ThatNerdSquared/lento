import 'package:flutter/material.dart';

import "cardtimer.dart";
import "cardtitle.dart";

// main lento card

class LentoCard extends StatelessWidget {
  const LentoCard({super.key}); // ?
  @override // ?

  Widget build(BuildContext context) {
    return SizedBox(
        width: 350.0,
        height: 450.0,
        child: Container(
            decoration: BoxDecoration(boxShadow: [
              BoxShadow(color: Colors.grey[300] as Color, blurRadius: 20.0)
            ]),
            child: Card(
                color: const Color(0xFFFFFFFF),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(20.0),
                ),
                child: const Padding(
                    padding: EdgeInsets.only(top: 10.0),
                    child: Column(
                        mainAxisAlignment: MainAxisAlignment.start,
                        children: [
                          CardTitle(),
                          Padding(padding: EdgeInsets.only(bottom: 10.0)),
                          CardTimer()
                        ])))));
  }
}
