import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:pret_a_porter/pret_a_porter.dart';

import '../config.dart';

class ToggleList extends ConsumerStatefulWidget {
  final String cardId;
  final String toggleTitle;
  final List<Widget> children;

  const ToggleList({
    super.key,
    required this.cardId,
    required this.toggleTitle,
    required this.children,
  });

  @override
  ToggleListState createState() => ToggleListState();
}

class ToggleListState extends ConsumerState<ToggleList> {
  bool opened = true;

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) => Container(
        margin: EdgeInsets.only(
          left: Config.defaultMarginPercentage * constraints.maxWidth,
          right: Config.defaultMarginPercentage * constraints.maxWidth,
        ),
        child: ClipRRect(
          borderRadius: PretConfig.defaultBorderRadius,
          child: ExpansionPanelList(
            expansionCallback: (index, isExpanded) {
              setState(() {
                opened = !isExpanded;
              });
            },
            children: [
              ExpansionPanel(
                backgroundColor: Theme.of(context).colorScheme.surface,
                isExpanded: opened,
                canTapOnHeader: true,
                headerBuilder: (context, isExpanded) => Container(
                  padding: const EdgeInsets.all(PretConfig.thinElementSpacing),
                  color: Theme.of(context).colorScheme.secondary,
                  child: Text(
                    widget.toggleTitle,
                    style: TextStyle(
                      color: Theme.of(context).colorScheme.onSecondary,
                    ),
                  ),
                ),
                body: Column(children: widget.children),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
