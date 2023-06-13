import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'cardtimer.dart';
import 'cardtitle.dart';
import 'config.dart';
import 'model/cardmodel.dart';

/// A card in the Lento deck.
class LentoCard extends StatelessWidget {
  final LentoCardModel lentoCard;

  const LentoCard({super.key, required this.lentoCard});

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
        create: (context) => lentoCard,
        child: SizedBox(
            width: 350.0,
            height: 450.0,
            child: Container(
                decoration: const BoxDecoration(
                    borderRadius: Config.defaultBorderRadius,
                    boxShadow: [Config.defaultShadow]),
                child: Card(
                    child: Padding(
                        padding:
                            const EdgeInsets.all(Config.defaultElementSpacing),
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
                            ]))))))));
  }
}
