import 'package:flutter/material.dart';

import 'cardtimer.dart';
import 'cardtitle.dart';
import 'config.dart';

/// A card in the Lento deck.
class LentoCard extends StatelessWidget {
  const LentoCard({super.key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
        width: 350.0,
        height: 450.0,
        child: Container(
            decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(Config.defaultBorderRadius),
                boxShadow: [
                  BoxShadow(
                      color: Theme.of(context).shadowColor,
                      offset: Config.defaultShadowOffset,
                      blurRadius: Config.defaultBlurRadius)
                ]),
            child: Card(
                child: Padding(
                    padding: const EdgeInsets.all(Config.defaultElementSpacing),
                    child: SingleChildScrollView(
                        child: Center(
                            child: Wrap(
                                direction: Axis.vertical,
                                spacing: Config.defaultElementSpacing,
                                children: [
                          const CardTitle(),
                          CardTimer(
                            startingColour:
                                Theme.of(context).colorScheme.surface,
                          )
                        ])))))));
  }
}
