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
    switch (blockItemTypeSelection) {
      case BlockItemType.website:
        final data = BlockedWebsiteData(
          siteUrl: Uri.parse(_urlTextFieldController.text),
          isRestrictedAccess: isAccessRestricted,
          customPopupId: selectedPopupId,
        );
        widget.editingEnv.blockItemId != null
            ? ref.read(lentoDeckProvider.notifier).updateBlockedWebsite(
                cardId: widget.editingEnv.cardId,
                blockItemId: widget.editingEnv.blockItemId!,
                newData: data)
            : ref.read(lentoDeckProvider.notifier).addBlockedWebsite(
                  cardId: widget.editingEnv.cardId,
                  websiteData: data,
                );
        break;
      case BlockItemType.app:
        final data = BlockedAppData(
          appName: basenameWithoutExtension(selectedApp!.path),
          sourcePaths: {Platform.operatingSystem: selectedApp!.path},
          isRestrictedAccess: isAccessRestricted,
          customPopupId: selectedPopupId,
        );
        widget.editingEnv.blockItemId != null
            ? ref.read(lentoDeckProvider.notifier).updateBlockedApp(
                cardId: widget.editingEnv.cardId,
                blockItemId: widget.editingEnv.blockItemId!,
                newData: data)
            : ref.read(lentoDeckProvider.notifier).addBlockedApp(
                  cardId: widget.editingEnv.cardId,
                  appData: data,
                );
        break;
    }
    widget.endEditing();
  }

  @override
  Widget build(BuildContext context) {
    var popups = ref.watch(customPopupListProvider);
    if (widget.editingEnv.blockItemType != null && !processedData) {
      toggleBlockItemType(widget.editingEnv.blockItemType);
      switch (widget.editingEnv.blockItemType!) {
        case BlockItemType.app:
          final item = ref
              .read(lentoDeckProvider)[widget.editingEnv.cardId]!
              .blockedApps[widget.editingEnv.blockItemId];
          setState(() {
            selectedApp = File(item!.currentSourcePath!);
            isAccessRestricted = item.isRestrictedAccess;
            selectedPopupId = item.customPopupId;
          });
        case BlockItemType.website:
          final item = ref
              .read(lentoDeckProvider)[widget.editingEnv.cardId]!
              .blockedSites[widget.editingEnv.blockItemId];
          setState(() {
            _urlTextFieldController.text = item!.siteUrl.toString();
            isAccessRestricted = item.isRestrictedAccess;
            selectedPopupId = item.customPopupId;
          });
      }
    }
    setState(() {
      processedData = true;
    });
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
                    child: Form(
                      key: _formKey,
                      child: Column(
                        children: [
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              CupertinoButton.filled(
                                onPressed: widget.endEditing,
                                child: Text(
                                  'Cancel',
                                  style: Theme.of(context)
                                      .textTheme
                                      .labelLarge!
                                      .copyWith(
                                          color: Theme.of(context)
                                              .colorScheme
                                              .error),
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
                                      .copyWith(
                                          color: Theme.of(context)
                                              .colorScheme
                                              .tertiary),
                                ),
                              )
                            ],
                          ),
                          Expanded(
                              child: CustomScrollView(
                            slivers: [
                              SliverToBoxAdapter(
                                  child: Text(
                                'Block something...',
                                textAlign: TextAlign.center,
                                style:
                                    Theme.of(context).textTheme.displayMedium,
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
                                    onValueChanged: toggleBlockItemType),
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
                                              BlockItemType.app
                                          ? FormField(
                                              validator: (_) => (selectedApp ==
                                                          null &&
                                                      blockItemTypeSelection ==
                                                          BlockItemType.app)
                                                  ? 'Please choose an app to block!'
                                                  : null,
                                              builder: (_) => Column(children: [
                                                    Container(
                                                      decoration:
                                                          const BoxDecoration(
                                                              boxShadow: [
                                                            PretConfig
                                                                .defaultShadow
                                                          ]),
                                                      child: TextButton(
                                                        onPressed: () async {
                                                          var selection =
                                                              await showAppPicker();
                                                          setState(() {
                                                            selectedApp =
                                                                selection;
                                                          });
                                                        },
                                                        style: ButtonStyle(
                                                            backgroundColor:
                                                                MaterialStatePropertyAll(Theme.of(
                                                                        context)
                                                                    .colorScheme
                                                                    .tertiary),
                                                            padding: const MaterialStatePropertyAll(
                                                                EdgeInsets.all(
                                                                    PretConfig
                                                                        .defaultElementSpacing)),
                                                            shape: const MaterialStatePropertyAll(
                                                                RoundedRectangleBorder(
                                                                    borderRadius:
                                                                        PretConfig
                                                                            .thinBorderRadius))),
                                                        child: const Text(
                                                            'Choose app...'),
                                                      ),
                                                    ),
                                                    const Padding(
                                                        padding: EdgeInsets.all(
                                                            PretConfig
                                                                .minElementSpacing)),
                                                    Text(
                                                      selectedApp != null
                                                          ? basename(
                                                              selectedApp!.path)
                                                          : 'No app selected',
                                                      style: Theme.of(context)
                                                          .textTheme
                                                          .labelMedium!
                                                          .copyWith(
                                                              color: Theme.of(
                                                                      context)
                                                                  .colorScheme
                                                                  .tertiary),
                                                    )
                                                  ]))
                                          : TextFormField(
                                              controller:
                                                  _urlTextFieldController,
                                              validator: (value) => (value!
                                                          .isEmpty &&
                                                      blockItemTypeSelection ==
                                                          BlockItemType.website)
                                                  ? 'Please enter a URL to block!'
                                                  : null,
                                              textAlign: TextAlign.center,
                                              style: Theme.of(context)
                                                  .textTheme
                                                  .labelLarge,
                                              decoration: const InputDecoration(
                                                  border: InputBorder.none,
                                                  hintText: 'youtube.com'),
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
                                          Text(
                                            'Restricted Access',
                                            style: Theme.of(context)
                                                .textTheme
                                                .labelLarge,
                                          ),
                                          PretTooltip(
                                              maxWidth: 300,
                                              tooltipContent: Text(
                                                'Allow access to the blocked site or app in 15 minute intervals, instead of blocking it right away.',
                                                style: Theme.of(context)
                                                    .textTheme
                                                    .labelSmall,
                                              ),
                                              icon: const FaIcon(
                                                  FontAwesomeIcons
                                                      .circleQuestion)),
                                          const Spacer(),
                                          CupertinoSwitch(
                                              value: isAccessRestricted,
                                              onChanged: (value) =>
                                                  setState(() {
                                                    isAccessRestricted = value;
                                                  }))
                                        ],
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
                                child: Text(
                                  'Add a custom popup message:',
                                  style: Theme.of(context).textTheme.labelLarge,
                                ),
                              )),
                              const SliverPadding(
                                  padding: EdgeInsets.only(
                                      top: PretConfig.defaultElementSpacing)),
                              SliverList.builder(
                                itemCount: popups.length,
                                itemBuilder: (context, index) {
                                  var itemId = popups.keys.elementAt(index);
                                  var message = popups[itemId]!.customMessage;
                                  return Padding(
                                      padding: EdgeInsets.only(
                                        left: Config.defaultMarginPercentage *
                                            constraints.maxWidth,
                                        right: Config.defaultMarginPercentage *
                                            constraints.maxWidth,
                                      ),
                                      child: GestureDetector(
                                        onTap: () {
                                          setState(() {
                                            selectedPopupId != itemId
                                                ? selectedPopupId = itemId
                                                : selectedPopupId = null;
                                          });
                                        },
                                        child: PretCard(
                                          borderColor: selectedPopupId == itemId
                                              ? Theme.of(context)
                                                  .colorScheme
                                                  .tertiary
                                              : null,
                                          child: Text(
                                            message,
                                            style: Theme.of(context)
                                                .textTheme
                                                .bodyMedium,
                                          ),
                                        ),
                                      ));
                                },
                              )
                            ],
                          ))
                        ],
                      ),
                    )),
              ),
            ));
  }
}
