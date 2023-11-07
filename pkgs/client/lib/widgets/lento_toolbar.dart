import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../main.dart';

class LentoToolbar extends ConsumerWidget {
  final int currentCardIndex;
  final VoidCallback nextPageHandler;
  final VoidCallback prevPageHandler;

  const LentoToolbar({
    super.key,
    required this.currentCardIndex,
    required this.nextPageHandler,
    required this.prevPageHandler,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    var currentCardId =
        ref.watch(lentoDeckProvider).keys.elementAt(currentCardIndex);
    return LayoutBuilder(
      builder: ((context, constraints) => Row(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              IconButton(
                iconSize: 0.4 * constraints.maxHeight,
                onPressed: () {
                  ref.read(lentoDeckProvider.notifier).addNewCard();
                  nextPageHandler();
                },
                icon: const Icon(Icons.add),
              ),
              IconButton(
                iconSize: 0.4 * constraints.maxHeight,
                onPressed: () {
                  ref
                      .read(lentoDeckProvider.notifier)
                      .removeCard(cardId: currentCardId);
                  ref.read(lentoDeckProvider).entries.isEmpty
                      ? ref.read(lentoDeckProvider.notifier).addNewCard()
                      : null;
                  prevPageHandler();
                },
                icon: const Icon(Icons.delete_outline),
              ),
            ],
          )),
    );
  }
}
