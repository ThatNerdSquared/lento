import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:uuid/uuid.dart';

import 'config.dart';
import 'model/cardmodel.dart';
import 'widgets/card.dart';

const uuID = Uuid();

final mockIds = [uuID.v4(), uuID.v4(), uuID.v4()];
final lentoDeckProvider =
    StateNotifierProvider<LentoDeck, Map<String, LentoCardData>>((ref) {
  return LentoDeck(initialDeck: {
    mockIds[0]: const LentoCardData(),
    mockIds[1]: const LentoCardData(cardName: 'Card 2'),
    mockIds[2]: const LentoCardData(cardName: 'code wrangling'),
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
          shadowColor: lentoLightColorScheme.shadow),
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
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Center(
      child: Column(
        children: [
          SizedBox(
              width: 350.0,
              height: 450.0,
              child: PageView.builder(
                  itemBuilder: (context, index) => LentoCard(
                        cardId:
                            ref.read(lentoDeckProvider).keys.elementAt(index),
                      )))
        ],
      ),
    ));
  }
}
