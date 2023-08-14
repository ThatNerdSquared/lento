import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../backend/card_data.dart';

class BlockListItem extends ConsumerWidget {
  final String itemTitle;
  final bool isAccessRestricted;
  final bool isEnabled;

  BlockListItem.fromBlockedWebsite(
      {super.key, required BlockedWebsiteData data})
      : itemTitle = data.siteUrl.host,
        isAccessRestricted = data.isAccessRestricted,
        isEnabled = data.isEnabled;

  BlockListItem.fromBlockedApp({super.key, required BlockedAppData data})
      : itemTitle = data.appName,
        isAccessRestricted = data.isAccessRestricted,
        isEnabled = data.isEnabled;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return ListTile(
      leading: Checkbox.adaptive(
        value: isEnabled,
        onChanged: (_) => print('untoggle'),
      ),
      title: Row(
        children: [
          const Icon(Icons.archive),
          Text(itemTitle),
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
