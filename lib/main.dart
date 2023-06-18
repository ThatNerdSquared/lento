import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:uuid/uuid.dart';

import 'card.dart';
import 'config.dart';
import 'model/cardmodel.dart';

final lentoDeckProvider =
    StateNotifierProvider<LentoDeck, List<LentoCardData>>((ref) {
  return LentoDeck(initialDeck: [
    LentoCardData(cardId: uuID.v4()),
    LentoCardData(cardId: uuID.v4(), cardName: 'Card 2'),
    LentoCardData(cardId: uuID.v4(), cardName: 'code wrangling')
  ]);
});

const uuID = Uuid();

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
                      cardId: ref.read(lentoDeckProvider)[index].cardId,
                      idx: index)))
        ],
      ),
    ));
  }
}
