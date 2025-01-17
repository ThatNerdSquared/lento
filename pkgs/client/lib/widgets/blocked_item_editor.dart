import 'dart:io';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:path/path.dart';
import 'package:pret_a_porter/pret_a_porter.dart';

import '../backend/card_data.dart';
import '../config.dart';
import '../main.dart';
import 'app_picker.dart';
import 'card.dart';
import 'popup_msg_form.dart';

@immutable
class EditingEnv {
  final String cardId;
  final String? blockItemId;
  final BlockItemType? blockItemType;

  const EditingEnv({
    required this.cardId,
    required this.blockItemId,
    required this.blockItemType,
  });
}

const Map<BlockItemType, Text> blockItemTypeWidgets = {
  BlockItemType.website: Text('Website'),
  BlockItemType.app: Text('App'),
};

/// an editor for creating and editing blockitems, both website and apps.
/// at some point we should probably revisit how we're handling this -
/// i think it might be better for us to handle different BlockItem types
/// via abstract classes or something. although if we end up combining
/// the different blockitem types this might become irrelevant. we'll see.
class BlockedItemEditor extends ConsumerStatefulWidget {
  final EditingEnv editingEnv;
  final VoidCallback endEditing;

  BlockedItemEditor({
    super.key,
    required this.editingEnv,
    required this.endEditing,
  }) {
    if ((editingEnv.blockItemType == null) ^ (editingEnv.blockItemId == null)) {
      throw ArgumentError(
        'Block item type and block item id cannot have different null/non-null states!',
      );
    }
  }

  @override
  BlockedItemEditorState createState() => BlockedItemEditorState();
}

class BlockedItemEditorState extends ConsumerState<BlockedItemEditor> {
  final _formKey = GlobalKey<FormState>();
  final _urlTextFieldController = TextEditingController();
  BlockItemType blockItemTypeSelection = BlockItemType.website;

  bool isAccessRestricted = false;
  File? selectedApp;
  String? selectedPopupId;

  bool processedData = false;

  void toggleBlockItemType(BlockItemType? value) => setState(() {
        value != null ? blockItemTypeSelection = value : null;
      });

  void onSubmitItem(WidgetRef ref) {
    if (!_formKey.currentState!.validate()) return;
    final data = switch (blockItemTypeSelection) {
      BlockItemType.app => BlockedItemData(
          type: BlockItemType.app,
          itemName: basenameWithoutExtension(selectedApp!.path),
          sourcePaths: {Platform.operatingSystem: selectedApp!.path},
          isEnabled: true,
          isRestrictedAccess: isAccessRestricted,
          customPopupId: selectedPopupId,
        ),
      BlockItemType.website => BlockedItemData(
          type: BlockItemType.website,
          itemName: Uri.parse(_urlTextFieldController.text).host,
          sourcePaths: {'_website': _urlTextFieldController.text},
          isEnabled: true,
          isRestrictedAccess: isAccessRestricted,
          customPopupId: selectedPopupId,
        ),
    };
    widget.editingEnv.blockItemId != null
        ? ref.read(lentoDeckProvider.notifier).updateBlockedItem(
            cardId: widget.editingEnv.cardId,
            blockItemId: widget.editingEnv.blockItemId!,
            newData: data)
        : ref.read(lentoDeckProvider.notifier).addBlockedItem(
              cardId: widget.editingEnv.cardId,
              blockedItem: data,
            );
    widget.endEditing();
  }

  @override
  Widget build(BuildContext context) {
    final popups = ref.watch(popupMsgsProvider);
    if (widget.editingEnv.blockItemType != null && !processedData) {
      toggleBlockItemType(widget.editingEnv.blockItemType);
      final item = ref
          .read(lentoDeckProvider)[widget.editingEnv.cardId]!
          .blockedItems[widget.editingEnv.blockItemId];
      setState(switch (widget.editingEnv.blockItemType!) {
        BlockItemType.app => () {
            selectedApp = File(item!.currentSourcePath!);
            isAccessRestricted = item.isRestrictedAccess;
            selectedPopupId = item.customPopupId;
          },
        BlockItemType.website => () {
            _urlTextFieldController.text = item!.currentSourcePath!;
            isAccessRestricted = item.isRestrictedAccess;
            selectedPopupId = item.customPopupId;
          }
      });
    }
    setState(() {
      processedData = true;
    });
    return LayoutBuilder(builder: (context, constraints) {
      final defaultEdgeInsets = EdgeInsets.only(
        left: Config.defaultMarginPercentage * constraints.maxWidth,
        right: Config.defaultMarginPercentage * constraints.maxWidth,
      );
      return StyledCard(
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              EditorCancelOkBar(
                endEditing: widget.endEditing,
                onSubmitItem: onSubmitItem,
              ),
              Expanded(
                  child: CustomScrollView(
                slivers: [
                  SliverToBoxAdapter(
                    child: Text(
                      'Block something...',
                      textAlign: TextAlign.center,
                      style: Theme.of(context).textTheme.displayMedium,
                    ),
                  ),
                  Config.defaultSliverPadding,
                  SliverToBoxAdapter(
                    child: Container(
                      margin: defaultEdgeInsets,
                      child: CupertinoSlidingSegmentedControl(
                          children: blockItemTypeWidgets,
                          groupValue: blockItemTypeSelection,
                          onValueChanged: toggleBlockItemType),
                    ),
                  ),
                  Config.defaultSliverPadding,
                  SliverToBoxAdapter(
                    child: Container(
                      margin: defaultEdgeInsets,
                      child: blockItemTypeSelection == BlockItemType.app
                          ? AppSelectionForm(
                              selectedApp: selectedApp,
                              blockItemTypeSelection: blockItemTypeSelection,
                              selectedAppSetter: (selection) => setState(() {
                                selectedApp = selection;
                              }),
                            )
                          : TextFormField(
                              controller: _urlTextFieldController,
                              validator: (value) => (value!.isEmpty &&
                                      blockItemTypeSelection ==
                                          BlockItemType.website)
                                  ? 'Please enter a URL to block!'
                                  : null,
                              textAlign: TextAlign.center,
                              style: Theme.of(context).textTheme.labelLarge,
                              cursorColor: Colors.grey,
                              decoration: const InputDecoration(
                                  border: OutlineInputBorder(
                                    borderRadius:
                                        PretConfig.defaultBorderRadius,
                                    borderSide: BorderSide.none,
                                  ),
                                  filled: true,
                                  hintText: 'youtube.com'),
                            ),
                    ),
                  ),
                  Config.defaultSliverPadding,
                  SliverToBoxAdapter(
                      child: RestrictedAccessFormField(
                    defaultEdgeInsets: defaultEdgeInsets,
                    isAccessRestricted: isAccessRestricted,
                    toggleRestrictedAccessHandler: ({required newData}) =>
                        setState(() {
                      isAccessRestricted = newData;
                    }),
                  )),
                  Config.defaultSliverPadding,
                  SliverToBoxAdapter(
                      child: Container(
                    margin: defaultEdgeInsets,
                    child: Text(
                      'Add a custom popup message:',
                      style: Theme.of(context).textTheme.labelLarge,
                    ),
                  )),
                  Config.defaultSliverPadding,
                  SliverToBoxAdapter(
                    child: Container(
                      margin: defaultEdgeInsets,
                      child: OnelineTextAddForm(
                        handleSubmit: (text) =>
                            ref.read(popupMsgsProvider.notifier).addPopup(text),
                        hintText: 'Don\'t get distracted!',
                        validatorErrorMsg: 'Please enter a popup message!',
                      ),
                    ),
                  ),
                  SliverList.builder(
                    itemCount: popups.length,
                    itemBuilder: (context, index) {
                      final itemId = popups.keys.elementAt(index);
                      final message = popups[itemId];
                      return Padding(
                          padding: defaultEdgeInsets,
                          child: GestureDetector(
                            onTap: () {
                              setState(() {
                                selectedPopupId != itemId
                                    ? selectedPopupId = itemId
                                    : selectedPopupId = null;
                              });
                            },
                            child: ContextMenuRegion(
                              contextMenu: popupMsgContextMenu(ref, itemId),
                              child: PretCard(
                                borderColor: selectedPopupId == itemId
                                    ? Theme.of(context).colorScheme.tertiary
                                    : null,
                                child: Text(
                                  message!,
                                  style: Theme.of(context).textTheme.bodyMedium,
                                ),
                              ),
                            ),
                          ));
                    },
                  )
                ],
              ))
            ],
          ),
        ),
      );
    });
  }
}

class RestrictedAccessFormField extends StatelessWidget {
  const RestrictedAccessFormField({
    super.key,
    required this.defaultEdgeInsets,
    required this.isAccessRestricted,
    required this.toggleRestrictedAccessHandler,
  });

  final EdgeInsets defaultEdgeInsets;
  final bool isAccessRestricted;
  final Function({required bool newData}) toggleRestrictedAccessHandler;

  @override
  Widget build(BuildContext context) {
    return Container(
        margin: defaultEdgeInsets,
        child: Row(
          children: [
            Text(
              'Restricted Access',
              style: Theme.of(context).textTheme.labelLarge,
            ),
            PretTooltip(
                maxWidth: 300,
                tooltipContent: Text(
                  'Allow access to the blocked site or app in 15 minute intervals, instead of blocking it right away.',
                  style: Theme.of(context).textTheme.labelSmall,
                ),
                icon: const FaIcon(FontAwesomeIcons.circleQuestion)),
            const Spacer(),
            CupertinoSwitch(
              value: isAccessRestricted,
              onChanged: (value) => toggleRestrictedAccessHandler(
                newData: value,
              ),
            )
          ],
        ));
  }
}

class EditorCancelOkBar extends ConsumerWidget {
  final VoidCallback endEditing;
  final Function(WidgetRef) onSubmitItem;

  const EditorCancelOkBar({
    super.key,
    required this.endEditing,
    required this.onSubmitItem,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) => Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          CupertinoButton.filled(
            onPressed: endEditing,
            child: Text(
              'Cancel',
              style: Theme.of(context)
                  .textTheme
                  .labelLarge!
                  .copyWith(color: Theme.of(context).colorScheme.error),
            ),
          ),
          CupertinoButton.filled(
            onPressed: () {
              onSubmitItem(ref);
            },
            child: Text(
              'OK',
              style: Theme.of(context)
                  .textTheme
                  .labelLarge!
                  .copyWith(color: Theme.of(context).colorScheme.tertiary),
            ),
          )
        ],
      );
}
