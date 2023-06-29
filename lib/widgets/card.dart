import 'package:flutter/material.dart';

import '../config.dart';
import 'card_timer.dart';
import 'card_title.dart';

/// A card in the Lento deck.
class LentoCard extends StatelessWidget {
  final String cardId;

  const LentoCard({super.key, required this.cardId});

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
        builder: (context, constraints) => Container(
            decoration: const BoxDecoration(
                borderRadius: Config.defaultBorderRadius,
                boxShadow: [Config.defaultShadow]),
            margin: const EdgeInsets.all(Config.defaultElementSpacing),
            child: Card(
                child: Padding(
              padding: const EdgeInsets.only(
                top: Config.defaultElementSpacing * 2,
              ),
              child: CustomScrollView(slivers: [
                SliverToBoxAdapter(
                    child: CardTitle(
                  cardId: cardId,
                )),
                SliverToBoxAdapter(
                    child: CardTimer(
                  cardId: cardId,
                  startingColour: Theme.of(context).colorScheme.surface,
                )),
              ]),
            ))));
  }
}
