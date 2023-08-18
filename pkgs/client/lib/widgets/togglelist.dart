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
  final List<Widget> children;

  const ToggleList({
    super.key,
    required this.cardId,
    required this.toggleTitle,
    required this.children,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return LayoutBuilder(
      builder: (context, constraints) => Container(
        margin: EdgeInsets.only(
          left: Config.defaultMarginPercentage * constraints.maxWidth,
          right: Config.defaultMarginPercentage * constraints.maxWidth,
        ),
        child: Stack(children: [
          Container(
            decoration: BoxDecoration(
              borderRadius: PretConfig.thinBorderRadius,
              color: Theme.of(context).colorScheme.secondary,
            ),
            height: 51,
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
                    style: TextStyle(
                      fontSize: 18,
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
                      children: children,
                    )),
              )),
        ]),
      ),
    );
  }
}
