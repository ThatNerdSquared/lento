import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../main.dart';

class LentoToolbar extends ConsumerWidget {
  final int currentCardIndex;

  const LentoToolbar({
    super.key,
    required this.currentCardIndex,
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
                onPressed: () =>
                    ref.read(lentoDeckProvider.notifier).addNewCard(),
                icon: const Icon(Icons.add),
              ),
              IconButton(
                iconSize: 0.4 * constraints.maxHeight,
                onPressed: () => ref
                    .read(lentoDeckProvider.notifier)
                    .removeCard(cardId: currentCardId),
                icon: const Icon(Icons.delete_outline),
              ),
            ],
          )),
    );
  }
}
