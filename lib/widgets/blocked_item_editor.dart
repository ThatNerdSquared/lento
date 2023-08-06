import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:pret_a_porter/pret_a_porter.dart';

class BlockedItemEditor extends ConsumerStatefulWidget {
  final String cardId;

  const BlockedItemEditor({
    super.key,
    required this.cardId,
  });

  @override
  BlockedItemEditorState createState() => BlockedItemEditorState();
}

class BlockedItemEditorState extends ConsumerState<BlockedItemEditor> {
  @override
  Widget build(BuildContext context) {
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
                      Text(
                        'Block a new item...',
                        style: Theme.of(context).textTheme.headlineSmall,
                      ),
                      ToggleButtons(isSelected: const [
                        true,
                        false
                      ], children: const [
                        Text('Website'),
                        Text('App'),
                      ])
                    ],
                  ),
                ),
              ),
            ));
  }
}
