import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:pret_a_porter/pret_a_porter.dart';

import '../config.dart';
import '../main.dart';
import 'blocklist_item.dart';
import 'card_timer.dart';
import 'card_title.dart';
import 'togglelist.dart';

/// A card in the Lento deck.
class LentoCard extends ConsumerWidget {
  final String cardId;
  final Function({
    String? blockItemId,
    BlockItemType? blockItemType,
  }) startEditing;

  const LentoCard({
    super.key,
    required this.cardId,
    required this.startEditing,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return LayoutBuilder(
        builder: (context, constraints) => Center(
                child: Container(
              decoration: const BoxDecoration(
                  borderRadius: PretConfig.defaultBorderRadius,
                  boxShadow: [PretConfig.defaultShadow]),
              margin: const EdgeInsets.all(PretConfig.defaultElementSpacing),
              child: Card(
                child: Padding(
                  padding: const EdgeInsets.only(
                    top: PretConfig.defaultElementSpacing * 2,
                    bottom: PretConfig.defaultElementSpacing * 2,
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
                                child: Container(
                              margin: const EdgeInsets.only(
                                top: PretConfig.defaultElementSpacing,
                              ),
                              child: ToggleList(
                                  cardId: cardId,
                                  toggleTitle: 'Blocked Websites',
                                  emptyLabel: 'No blocked websites',
                                  children: ref
                                      .watch(lentoDeckProvider)[cardId]!
                                      .blockedSites
                                      .entries
                                      .map((item) =>
                                          BlockListItem.fromBlockedWebsite(
                                            cardId: cardId,
                                            itemID: item.key,
                                            data: item.value,
                                            startEditing: startEditing,
                                          ))
                                      .toList()),
                            )),
                            SliverToBoxAdapter(
                                child: Container(
                              margin: const EdgeInsets.only(
                                top: PretConfig.thinElementSpacing,
                              ),
                              child: ToggleList(
                                cardId: cardId,
                                toggleTitle: 'Blocked Apps',
                                emptyLabel: 'No blocked apps',
                                children: ref
                                    .watch(lentoDeckProvider)[cardId]!
                                    .blockedApps
                                    .entries
                                    .map((item) => BlockListItem.fromBlockedApp(
                                          cardId: cardId,
                                          itemID: item.key,
                                          data: item.value,
                                          startEditing: startEditing,
                                        ))
                                    .toList(),
                              ),
                            )),
                          ])),
                      TextButton(
                        onPressed: startEditing,
                        child: Text(
                          '+ Block something...',
                          style: TextStyle(
                            color: Theme.of(context).colorScheme.onSurface,
                          ),
                        ),
                      )
                    ],
                  ),
                ),
              ),
            )));
  }
}
