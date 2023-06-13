import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'config.dart';
import 'model/cardmodel.dart';

/*
TODO:
- Text color
- Text hover
- Emoji picker?
*/

class CardTitle extends StatelessWidget {
  const CardTitle({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<LentoCardModel>(builder: (context, card, child) {
      Color? titleColor;
      // var cardName = Provider.of<LentoCardModel>(context, listen: false).cardName;
      // var updateCardTitle = Provider.of<LentoCardModel>(context, listen: false).updateCardTitle;
      return StatefulBuilder(
          builder: (context, setState) => MouseRegion(
              onHover: (pointer) {
                setState(() {
                  titleColor = Theme.of(context).colorScheme.surfaceTint;
                });
              },
              onExit: (pointer) {
                setState(() {
                  titleColor = Theme.of(context).colorScheme.primary;
                });
              },
              child: GestureDetector(
                  onTap: () {
                    setState(() {});
                  },
                  child: Container(
                      width: 280.0,
                      height: 50.0,
                      decoration: BoxDecoration(
                          color: titleColor,
                          borderRadius: Config.defaultBorderRadius),
                      child: TextFormField(
                          decoration: const InputDecoration(
                              border: InputBorder.none, hintText: 'Card name'),
                          textAlign: TextAlign.center,
                          initialValue: card.cardName,
                          onChanged: card.updateCardTitle)))));
    });
  }
}
//     });
//   }
// }