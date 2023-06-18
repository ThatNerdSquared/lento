import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'config.dart';
import 'main.dart';

/*
TODO:
- Text color
- Text hover
- Emoji picker?
*/

class CardTitle extends ConsumerWidget {
  final String cardId;
  final int idx;

  const CardTitle({super.key, required this.cardId, required this.idx});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    Color? titleColor;
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
                        initialValue:
                            ref.watch(lentoDeckProvider)[idx].cardName,
                        onChanged: (value) => ref
                            .read(lentoDeckProvider.notifier)
                            .updateCardTitle(cardId, value))))));
  }
}
//     });
//   }
// }
