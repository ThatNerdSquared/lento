import 'package:flutter/material.dart';

/*
TODO:
- Text color
- Text hover
- Emoji picker?
*/

class CardTitle extends StatefulWidget {
  const CardTitle({super.key});

  @override
  State<CardTitle> createState() => _CardTitleState();
}

class _CardTitleState extends State<CardTitle> {
  // bool _isClicked = true;
  final _titleController = TextEditingController(text: 'Untitled Card');
  bool _enabled = false;
  int count = 0;
  Color? _titleColor;

  @override
  Widget build(BuildContext context) {
    return MouseRegion(
        onHover: (pointer) {
          setState(() {
            _titleColor = Theme.of(context).colorScheme.surfaceTint;
          });
        },
        onExit: (pointer) {
          setState(() {
            count = 0;
            _enabled = false;
            _titleColor = null;
          });
        },
        child: GestureDetector(
            onTap: () {
              setState(() {
                _enabled = true;
              });
            },
            child: Container(
                width: 280.0,
                height: 50.0,
                decoration: BoxDecoration(
                    color: _titleColor,
                    borderRadius: const BorderRadius.all(Radius.circular(10))),
                child: TextField(
                    controller: _titleController,
                    enabled: _enabled,
                    textAlign: TextAlign.center,
                    decoration:
                        const InputDecoration(border: InputBorder.none)))));
  }

  void textEdit() {
    setState(() {
      _enabled = true;
    });
  }
}
