import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:pret_a_porter/pret_a_porter.dart';

import '../main.dart';
import 'card_timer.dart';
import 'card_title.dart';

/// A card in the Lento deck.
class LentoCard extends ConsumerWidget {
  final String cardId;
  final Function(String) startEditing;

  const LentoCard({
    super.key,
    required this.cardId,
    required this.startEditing,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return LayoutBuilder(
        builder: (context, constraints) => Container(
              decoration: const BoxDecoration(
                  borderRadius: PretConfig.defaultBorderRadius,
                  boxShadow: [PretConfig.defaultShadow]),
              margin: const EdgeInsets.all(PretConfig.defaultElementSpacing),
              child: Card(
                child: Padding(
                  padding: const EdgeInsets.only(
                    top: PretConfig.defaultElementSpacing * 2,
                    bottom: PretConfig.defaultElementSpacing,
                  ),
                  child: Column(
                    children: [
                      Expanded(
                          flex: 8,
                          child: CustomScrollView(slivers: [
                            SliverToBoxAdapter(
                                child: CardTitle(
                              cardId: cardId,
                            )),
                            SliverToBoxAdapter(
                                child: CardTimer(
                              cardId: cardId,
                              startingColour:
                                  Theme.of(context).colorScheme.surface,
                            )),
                            SliverToBoxAdapter(
                              child: PretToggleList(
                                items: ref
                                    .watch(lentoDeckProvider)[cardId]!
                                    .blockedSites
                                    .map((item) => ListTile(
                                          title: Text(item.siteUrl.toString()),
                                        )),
                                toggleTitle: 'Blocked Websites',
                              ),
                            )
                          ])),
                      TextButton(
                        onPressed: () => startEditing(cardId),
                        child: Text(
                          '+ Add an app or website',
                          style: TextStyle(
                            color: Theme.of(context).colorScheme.onSurface,
                          ),
                        ),
                      )
                    ],
                  ),
                ),
              ),
            ));
  }
}
