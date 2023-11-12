import 'dart:math';

import 'package:expandable/expandable.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:pret_a_porter/pret_a_porter.dart';

import '../config.dart';

class ToggleList extends ConsumerWidget {
  final String cardId;
  final String toggleTitle;
  final String emptyLabel;
  final List<Widget> additionalWidgets;
  final List<Widget> children;

  const ToggleList({
    super.key,
    required this.cardId,
    required this.toggleTitle,
    required this.emptyLabel,
    required this.children,
    this.additionalWidgets = const [],
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return LayoutBuilder(
      builder: (context, constraints) => Container(
        margin: EdgeInsets.only(
          top: PretConfig.thinElementSpacing,
          left: Config.defaultMarginPercentage * constraints.maxWidth,
          right: Config.defaultMarginPercentage * constraints.maxWidth,
        ),
        child: Stack(children: [
          Container(
            decoration: BoxDecoration(
              borderRadius: PretConfig.thinBorderRadius,
              color: Theme.of(context).colorScheme.secondary,
            ),
            height: 52,
          ),
          ExpandableTheme(
              data: const ExpandableThemeData(
                headerAlignment: ExpandablePanelHeaderAlignment.center,
                expandIcon: FontAwesomeIcons.caretRight,
                collapseIcon: FontAwesomeIcons.caretDown,
                iconPlacement: ExpandablePanelIconPlacement.left,
                iconRotationAngle: 0.5 * pi,
                iconSize: 30,
                useInkWell: false,
              ),
              child: ExpandablePanel(
                header: Container(
                  alignment: Alignment.centerLeft,
                  decoration: BoxDecoration(
                    color: Theme.of(context).colorScheme.secondary,
                    borderRadius: PretConfig.thinBorderRadius,
                  ),
                  padding:
                      const EdgeInsets.all(PretConfig.defaultElementSpacing),
                  child: Text(
                    toggleTitle,
                    style: Theme.of(context).textTheme.labelLarge!.copyWith(
                          color: Theme.of(context).colorScheme.onSecondary,
                        ),
                  ),
                ),
                collapsed: Container(),
                expanded: Container(
                    decoration: BoxDecoration(
                      color: Theme.of(context).colorScheme.surface,
                      borderRadius: PretConfig.thinBorderRadius,
                    ),
                    child: Column(
                      children: children.isEmpty
                          ? [
                              EmptyListLabel(labelText: emptyLabel),
                              ...additionalWidgets
                            ]
                          : [...children, ...additionalWidgets],
                    )),
              )),
        ]),
      ),
    );
  }
}

class EmptyListLabel extends StatelessWidget {
  final String labelText;

  const EmptyListLabel({
    super.key,
    required this.labelText,
  });

  @override
  Widget build(BuildContext context) {
    return Row(mainAxisAlignment: MainAxisAlignment.center, children: [
      Padding(
        padding: const EdgeInsets.all(PretConfig.defaultElementSpacing),
        child: Text(
          labelText,
          style: Theme.of(context).textTheme.labelSmall!.copyWith(
                fontStyle: FontStyle.italic,
                color: Theme.of(context).colorScheme.onSecondary,
              ),
        ),
      )
    ]);
  }
}
