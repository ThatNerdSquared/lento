import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../backend/card_data.dart';
import '../config.dart';
// import '../main.dart';

class BlockListItem extends ConsumerWidget {
  final String itemID;
  final String itemTitle;
  final bool isAccessRestricted;
  final bool isEnabled;
  final String sourcePath;
  final BlockItemType blockItemType;

  BlockListItem.fromBlockedWebsite({
    super.key,
    required this.itemID,
    required BlockedWebsiteData data,
  })  : itemTitle = data.siteUrl.host,
        isAccessRestricted = data.isAccessRestricted,
        isEnabled = data.isEnabled,
        sourcePath = data.siteUrl.toString(),
        blockItemType = BlockItemType.website;

  BlockListItem.fromBlockedApp({
    super.key,
    required this.itemID,
    required BlockedAppData data,
  })  : itemTitle = data.appName,
        isAccessRestricted = data.isAccessRestricted,
        isEnabled = data.isEnabled,
        sourcePath = data.currentSourcePath!,
        blockItemType = BlockItemType.website;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return ListTile(
      leading: Checkbox.adaptive(
        value: isEnabled,
        // ignore: avoid_print
        onChanged: (_) => print('untoggle'),
      ),
      title: Row(
        children: [
          const Icon(Icons.archive),
          // iconManager.loadIcon(itemID, blockItemType, sourcePath),
          Text(
            itemTitle,
            style: Theme.of(context).textTheme.labelMedium,
          ),
          if (isAccessRestricted)
            Icon(
              Icons.dangerous,
              color: Theme.of(context).colorScheme.error,
            ),
        ],
      ),
    );
  }
}
