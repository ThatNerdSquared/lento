import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:pret_a_porter/pret_a_porter.dart';

import '../backend/card_data.dart';
import '../config.dart';
import '../main.dart';

class BlockListItem extends ConsumerStatefulWidget {
  final String cardId;
  final String itemID;
  final String itemTitle;
  final bool isAccessRestricted;
  final bool isEnabled;
  final String sourcePath;
  final BlockItemType _blockItemType;

  BlockListItem.fromBlockedWebsite({
    super.key,
    required this.cardId,
    required this.itemID,
    required BlockedWebsiteData data,
  })  : itemTitle = data.siteUrl.host,
        isAccessRestricted = data.isRestrictedAccess,
        isEnabled = data.isEnabled,
        sourcePath = data.siteUrl.toString(),
        _blockItemType = BlockItemType.website;

  BlockListItem.fromBlockedApp({
    super.key,
    required this.cardId,
    required this.itemID,
    required BlockedAppData data,
  })  : itemTitle = data.appName,
        isAccessRestricted = data.isRestrictedAccess,
        isEnabled = data.isEnabled,
        sourcePath = data.currentSourcePath!,
        _blockItemType = BlockItemType.app;

  @override
  BlockListItemState createState() => BlockListItemState();
}

class BlockListItemState extends ConsumerState<BlockListItem> {
  Future<Widget> _loadIcon(iconId, srcPath) async {
    return switch (widget._blockItemType) {
      BlockItemType.app => await iconManager.loadAppIcon(iconId, srcPath),
      BlockItemType.website => await iconManager.loadWebsiteIcon(
          iconId,
          srcPath,
        ),
    };
  }

  Menu buildContextMenu() => Menu(items: [
        MenuItem.checkbox(
            label: 'Enable Restricted Access',
            checked: widget.isAccessRestricted,
            onClick: (_) => ref
                .read(lentoDeckProvider.notifier)
                .toggleRestrictedAccess(
                    cardId: widget.cardId, blockItemId: widget.itemID)),
        MenuItem(label: 'Edit Block Item'),
        MenuItem(
            label: 'Delete Block Item',
            onClick: (_) =>
                ref.read(lentoDeckProvider.notifier).deleteBlockItem(
                      cardId: widget.cardId,
                      blockItemId: widget.itemID,
                    ))
      ]);

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
        future: _loadIcon(widget.itemID, widget.sourcePath),
        builder: (context, snapshot) {
          return ContextMenuRegion(
              contextMenu: buildContextMenu(),
              child: ListTile(
                leading: Checkbox.adaptive(
                  value: widget.isEnabled,
                  // ignore: avoid_print
                  onChanged: (_) => print('untoggle'),
                ),
                title: Row(
                  children: [
                    snapshot.hasData
                        ? snapshot.data!
                        : const Icon(Icons.circle),
                    const Padding(
                      padding:
                          EdgeInsets.only(left: PretConfig.thinElementSpacing),
                    ),
                    Text(
                      widget.itemTitle,
                      style: Theme.of(context).textTheme.labelMedium,
                    ),
                    if (widget.isAccessRestricted)
                      Icon(
                        Icons.dangerous,
                        color: Theme.of(context).colorScheme.error,
                      ),
                  ],
                ),
              ));
        });
  }
}
