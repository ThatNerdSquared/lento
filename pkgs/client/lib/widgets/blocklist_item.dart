import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../backend/card_data.dart';
import '../config.dart';
import '../main.dart';

class BlockListItem extends ConsumerStatefulWidget {
  final String itemID;
  final String itemTitle;
  final bool isAccessRestricted;
  final bool isEnabled;
  final String sourcePath;
  final BlockItemType _blockItemType;

  BlockListItem.fromBlockedWebsite({
    super.key,
    required this.itemID,
    required BlockedWebsiteData data,
  })  : itemTitle = data.siteUrl.host,
        isAccessRestricted = data.isAccessRestricted,
        isEnabled = data.isEnabled,
        sourcePath = data.siteUrl.toString(),
        _blockItemType = BlockItemType.website;

  BlockListItem.fromBlockedApp({
    super.key,
    required this.itemID,
    required BlockedAppData data,
  })  : itemTitle = data.appName,
        isAccessRestricted = data.isAccessRestricted,
        isEnabled = data.isEnabled,
        sourcePath = data.currentSourcePath!,
        _blockItemType = BlockItemType.app;

  @override
  BlockListItemState createState() => BlockListItemState();
}

class BlockListItemState extends ConsumerState<BlockListItem> {
  Future<ImageIcon> _loadIcon(iconId, srcPath) async {
    return switch (widget._blockItemType) {
      BlockItemType.app => await iconManager.loadAppIcon(iconId, srcPath),
      BlockItemType.website => await iconManager.loadWebsiteIcon(
          iconId,
          srcPath,
        ),
    };
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
        future: _loadIcon(widget.itemID, widget.sourcePath),
        builder: (context, snapshot) {
          return ListTile(
            leading: Checkbox.adaptive(
              value: widget.isEnabled,
              // ignore: avoid_print
              onChanged: (_) => print('untoggle'),
            ),
            title: Row(
              children: [
                snapshot.hasData ? snapshot.data! : const Icon(Icons.circle),
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
          );
        });
  }
}
