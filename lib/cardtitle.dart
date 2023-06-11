import 'package:flutter/material.dart';

/*
TODO:
- Text color
- Text hover
- Emoji picker?

- Code styling, Check for "Dart correctness", etc
 */

class cardTitle extends StatefulWidget{
  const cardTitle({super.key});

  @override
  State<cardTitle> createState() => _cardTitleState();
}

class _cardTitleState extends State<cardTitle> {
  // bool _isClicked = true;
  var _title_controller = TextEditingController(text: "Untitled Card");
  bool _enabled = false;
  int count = 0;
  var _icon = Icon(Icons.edit);
  bool _edit_visibility = false;
  bool _buttonDisabled = false;
  var _titlePadding = EdgeInsets.zero;
  Color? _titleColor = null;


  @override
  Widget build(BuildContext context){
    return MouseRegion(
      onHover: (PointerEvent pointer){
        setState((){
        _edit_visibility = true;
        _titleColor = Color(0xFFeef2ef);
        });
      },
      onExit: (PointerEvent pointer){
        setState((){
          count = 0;
          _edit_visibility = false;
          _enabled = false;
          _icon = const Icon(Icons.edit);
          _titleColor = null;
          _titlePadding = EdgeInsets.zero;
        }
        );
      },

      child:
        GestureDetector(
          onTap: (){
            setState(() {
              _enabled = true;
            });
          },
          child:
            Container(
              width: 280.0,
              height: 50.0,
              decoration: BoxDecoration(
                color: _titleColor,
                borderRadius: BorderRadius.all(Radius.circular(10))
                ),
              child:
                TextField(
                  controller: _title_controller,
                  enabled: _enabled,
                  textAlign: TextAlign.center,
                  decoration: const InputDecoration(
                  border: InputBorder.none
                  )
                )
              )
            )
      );
    }

    void textEdit(){
      setState(() {
        _buttonDisabled = true;
        _enabled = true;
      });
    }
  }