import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../config.dart';

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
                  borderRadius: Config.defaultBorderRadius,
                  boxShadow: [Config.defaultShadow]),
              margin: const EdgeInsets.all(Config.defaultElementSpacing),
              child: Card(
                child: Padding(
                  padding: const EdgeInsets.only(
                    top: Config.defaultElementSpacing * 2,
                    bottom: Config.defaultElementSpacing,
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
