import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:uuid/uuid.dart';

import 'config.dart';
import 'model/cardmodel.dart';
import 'widgets/card.dart';
import 'widgets/lento_toolbar.dart';

const uuID = Uuid();

final mockIds = [uuID.v4(), uuID.v4(), uuID.v4()];
final lentoDeckProvider =
    StateNotifierProvider<LentoDeck, Map<String, LentoCardData>>((ref) {
  return LentoDeck(initialDeck: {
    mockIds[0]: const LentoCardData(
      blockDuration: CardTime.fromPresetTime(61),
    ),
    mockIds[1]: const LentoCardData(
      cardName: 'Card 2',
      blockDuration: CardTime.fromPresetTime(5),
    ),
    mockIds[2]: const LentoCardData(
      cardName: 'code wrangling',
    ),
  });
});

void main() {
  runApp(const ProviderScope(child: MyApp()));
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Lento',
      theme: ThemeData(
        cardTheme: lentoCardTheme,
        colorScheme: lentoLightColorScheme,
        scaffoldBackgroundColor: lentoLightColorScheme.background,
        shadowColor: lentoLightColorScheme.shadow,
      ),
      home: const LentoHome(title: 'Lento Home'),
    );
  }
}

class LentoHome extends ConsumerStatefulWidget {
  const LentoHome({super.key, required this.title});

  final String title;

  @override
  LentoHomeState createState() => LentoHomeState();
}

class LentoHomeState extends ConsumerState<LentoHome> {
  final PageController controller = PageController(
    viewportFraction: 0.8,
  );

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Center(
            child: Padding(
      padding: const EdgeInsets.only(top: Config.defaultElementSpacing),
      child: Column(
        children: [
          Flexible(
              flex: 5,
              child: Container(
                  constraints: const BoxConstraints(
                    maxWidth: 700.0,
                    maxHeight: 800.0,
                  ),
                  child: PageView.builder(
                      controller: controller,
                      itemBuilder: (context, index) => LentoCard(
                            cardId: ref
                                .read(lentoDeckProvider)
                                .keys
                                .elementAt(index),
                          )))),
          const Flexible(flex: 1, child: LentoToolbar()),
        ],
      ),
    )));
  }
}
