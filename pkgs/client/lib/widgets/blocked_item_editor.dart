import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:pret_a_porter/pret_a_porter.dart';

import '../config.dart';

enum BlockItemTypes { website, app }

const Map<BlockItemTypes, Text> blockItemTypeWidgets = {
  BlockItemTypes.website: Text('Website'),
  BlockItemTypes.app: Text('App'),
};

class BlockedItemEditor extends ConsumerStatefulWidget {
  final String cardId;
  final Function() endEditing;

  const BlockedItemEditor({
    super.key,
    required this.cardId,
    required this.endEditing,
  });

  @override
  BlockedItemEditorState createState() => BlockedItemEditorState();
}

class BlockedItemEditorState extends ConsumerState<BlockedItemEditor> {
  BlockItemTypes blockItemTypeSelection = BlockItemTypes.website;
  bool isAccessRestricted = false;

  void onSubmitItem() {
    print('test');
  }

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
                    top: PretConfig.defaultElementSpacing,
                    bottom: PretConfig.defaultElementSpacing,
                  ),
                  child: Column(
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          CupertinoButton.filled(
                            onPressed: widget.endEditing,
                            child: Text(
                              'Cancel',
                              style: TextStyle(
                                  color: Theme.of(context).colorScheme.error),
                            ),
                          ),
                          CupertinoButton.filled(
                            onPressed: onSubmitItem,
                            child: Text(
                              'OK',
                              style: TextStyle(
                                  color:
                                      Theme.of(context).colorScheme.tertiary),
                            ),
                          )
                        ],
                      ),
                      Expanded(
                          child: CustomScrollView(
                        slivers: [
                          const SliverToBoxAdapter(
                              child: Text(
                            'Block a new item...',
                            textAlign: TextAlign.center,
                            style: TextStyle(
                              fontWeight: FontWeight.w600,
                              fontSize: 30,
                            ),
                          )),
                          const SliverPadding(
                              padding: EdgeInsets.only(
                                  top: PretConfig.defaultElementSpacing)),
                          SliverToBoxAdapter(
                              child: Container(
                            margin: EdgeInsets.only(
                              left: Config.defaultMarginPercentage *
                                  constraints.maxWidth,
                              right: Config.defaultMarginPercentage *
                                  constraints.maxWidth,
                            ),
                            child: CupertinoSlidingSegmentedControl(
                                children: blockItemTypeWidgets,
                                groupValue: blockItemTypeSelection,
                                onValueChanged: (value) => setState(() {
                                      value != null
                                          ? blockItemTypeSelection = value
                                          : null;
                                    })),
                          )),
                          const SliverPadding(
                              padding: EdgeInsets.only(
                                  top: PretConfig.defaultElementSpacing)),
                          SliverToBoxAdapter(
                              child: Container(
                                  margin: EdgeInsets.only(
                                    left: Config.defaultMarginPercentage *
                                        constraints.maxWidth,
                                    right: Config.defaultMarginPercentage *
                                        constraints.maxWidth,
                                  ),
                                  child: blockItemTypeSelection ==
                                          BlockItemTypes.app
                                      ? ElevatedButton(
                                          onPressed: () => print('item'),
                                          child: const Text('Choose app...'))
                                      : TextFormField(
                                          textAlign: TextAlign.center,
                                          decoration: const InputDecoration(
                                              border: InputBorder.none,
                                              hintText: 'https://youtube.com'),
                                        ))),
                          const SliverPadding(
                              padding: EdgeInsets.only(
                                  top: PretConfig.defaultElementSpacing)),
                          SliverToBoxAdapter(
                              child: Container(
                                  margin: EdgeInsets.only(
                                    left: Config.defaultMarginPercentage *
                                        constraints.maxWidth,
                                    right: Config.defaultMarginPercentage *
                                        constraints.maxWidth,
                                  ),
                                  child: Row(
                                    children: [
                                      const Text('Restricted Access'),
                                      Tooltip(
                                        padding: const EdgeInsets.all(
                                            PretConfig.defaultElementSpacing),
                                        decoration: BoxDecoration(
                                          color: Theme.of(context)
                                              .colorScheme
                                              .primary,
                                          borderRadius:
                                              PretConfig.defaultBorderRadius,
                                          boxShadow: const [
                                            PretConfig.defaultShadow
                                          ],
                                        ),
                                        richMessage: WidgetSpan(
                                            child: ConstrainedBox(
                                          constraints: const BoxConstraints(
                                              maxWidth: 300),
                                          child: const Text(
                                              // 'Show a prompt to confirm you want to visit the blocked site or app, instead of blocking it right away.'),
                                              'Allow access to the blocked site or app in 15 minute intervals, instead of blocking it right away.'),
                                        )),
                                        child: const Icon(Icons.question_mark),
                                      ),
                                      const Spacer(),
                                      CupertinoSwitch(
                                          value: isAccessRestricted,
                                          onChanged: (value) => setState(() {
                                                isAccessRestricted = value;
                                              }))
                                    ],
                                  )))
                        ],
                      ))
                    ],
                  ),
                ),
              ),
            ));
  }
}
