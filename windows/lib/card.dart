import 'package:flutter/material.dart';

class LentoCard extends StatelessWidget{
  const LentoCard({super.key}); // ?

  @override // ?
  
  Widget build(BuildContext context){
    return SizedBox(
        width: 500.0,
        height: 300.0,
        child:
            Card(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      "hello",
                      textAlign: TextAlign.center
                    )
                  ]
                )
              )
      );
  }

}