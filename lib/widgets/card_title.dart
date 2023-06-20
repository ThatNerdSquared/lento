import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../config.dart';
import '../main.dart';

/*
TODO:
- Text color
- Text hover
- Emoji picker?
*/

class CardTitle extends ConsumerWidget {
  final String cardId;

  const CardTitle({super.key, required this.cardId});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    Color? titleColor;
    var isCardActivated = ref
        .watch(lentoDeckProvider.select((deck) => deck[cardId]!.isActivated));
    return StatefulBuilder(
        builder: (context, setState) => MouseRegion(
            onHover: (pointer) {
              if (!isCardActivated) {
                setState(() {
                  titleColor = Theme.of(context).colorScheme.surfaceTint;
                });
              }
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
                        enabled: !isCardActivated,
                        decoration: const InputDecoration(
                            border: InputBorder.none, hintText: 'Card name'),
                        textAlign: TextAlign.center,
                        initialValue: ref.watch(lentoDeckProvider
                            .select((deck) => deck[cardId]!.cardName)),
                        onChanged: (value) => ref
                            .read(lentoDeckProvider.notifier)
                            .updateCardTitle(cardId, value))))));
  }
}
//     });
//   }
// }
