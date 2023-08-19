import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:pret_a_porter/pret_a_porter.dart';

import '../config.dart';
import '../main.dart';

class CardTitle extends ConsumerStatefulWidget {
  final String cardId;

  const CardTitle({super.key, required this.cardId});

  @override
  CardTitleState createState() => CardTitleState();
}

class CardTitleState extends ConsumerState<CardTitle> {
  Color? titleColor;
  @override
  Widget build(BuildContext context) {
    var isCardActivated = ref.watch(
        lentoDeckProvider.select((deck) => deck[widget.cardId]!.isActivated));
    return LayoutBuilder(
        builder: (context, constraints) => MouseRegion(
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
                  setState(() {
                    titleColor = Theme.of(context).colorScheme.surfaceTint;
                  });
                },
                child: Container(
                    decoration: BoxDecoration(
                        color: titleColor,
                        borderRadius: PretConfig.defaultBorderRadius),
                    margin: EdgeInsets.only(
                      left:
                          Config.defaultMarginPercentage * constraints.maxWidth,
                      right:
                          Config.defaultMarginPercentage * constraints.maxWidth,
                      bottom: PretConfig.defaultElementSpacing,
                    ),
                    child: TextFormField(
                        enabled: !isCardActivated,
                        decoration: const InputDecoration(
                            border: InputBorder.none, hintText: 'Card name'),
                        textAlign: TextAlign.center,
                        cursorColor: Colors.grey,
                        style: Theme.of(context).textTheme.displayMedium,
                        initialValue: ref.watch(lentoDeckProvider
                            .select((deck) => deck[widget.cardId]!.cardName)),
                        onChanged: (value) => ref
                            .read(lentoDeckProvider.notifier)
                            .updateCardTitle(widget.cardId, value))))));
  }
}
