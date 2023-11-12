import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:pret_a_porter/pret_a_porter.dart';

import '../config.dart';
import '../main.dart';
import 'blocklist_item.dart';
import 'card_timer.dart';
import 'card_title.dart';
import 'popup_msg_form.dart';
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
  Widget build(BuildContext context, WidgetRef ref) => StyledCard(
        child: Column(
          children: [
            Expanded(
                flex: 8,
                child: CustomScrollView(
                    slivers: [
                  CardTitle(
                    cardId: cardId,
                  ),
                  CardTimer(
                    cardId: cardId,
                    startingColour: Theme.of(context).colorScheme.surface,
                  ),
                  ToggleList(
                      cardId: cardId,
                      toggleTitle: 'Blocked Websites',
                      emptyLabel: 'No blocked websites',
                      children: ref
                          .watch(lentoDeckProvider)[cardId]!
                          .blockedSites
                          .entries
                          .map((item) => BlockListItem.fromBlockedWebsite(
                                cardId: cardId,
                                itemID: item.key,
                                data: item.value,
                                startEditing: startEditing,
                              ))
                          .toList()),
                  ToggleList(
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
                  ToggleList(
                    cardId: cardId,
                    toggleTitle: 'To-do',
                    emptyLabel: 'No to-dos',
                    additionalWidgets: [
                      OnelineTextAddForm(
                        handleSubmit: (text) => ref
                            .read(lentoDeckProvider.notifier)
                            .addTodo(cardId: cardId, title: text),
                        hintText: 'What\'s on your plate?',
                        validatorErrorMsg: 'Please enter a todo!',
                      ),
                      const Padding(
                        padding: EdgeInsets.only(
                          bottom: PretConfig.minElementSpacing,
                        ),
                      ),
                    ],
                    children: ref
                        .watch(lentoDeckProvider)[cardId]!
                        .todos
                        .entries
                        .map((item) => TodoListItem(
                              cardId: cardId,
                              todoId: item.key,
                              todo: item.value,
                            ))
                        .toList(),
                  ),
                  const Padding(
                    padding: EdgeInsets.all(PretConfig.defaultElementSpacing),
                  ),
                ].map((widget) => SliverToBoxAdapter(child: widget)).toList())),
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
      );
}

class StyledCard extends StatelessWidget {
  final Widget child;

  const StyledCard({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
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
              child: child,
            ),
          ),
        ),
      ),
    );
  }
}
