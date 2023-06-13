import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'card.dart';
import 'config.dart';
import 'model/cardmodel.dart';

void main() {
  runApp(const MyApp());
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

class LentoHome extends StatefulWidget {
  const LentoHome({super.key, required this.title});

  final String title;

  @override
  State<LentoHome> createState() => _LentoHomeState();
}

class _LentoHomeState extends State<LentoHome> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Center(
            child: ChangeNotifierProvider(
      create: (context) => LentoDeckModel(cards: [LentoCardModel()]),
      child: Column(
        children: [
          SizedBox(
              width: 350.0,
              height: 450.0,
              // child: PageView.builder(
              //     itemBuilder: (context, index) => ChangeNotifierProvider(
              //         create: (context) =>
              //             Provider.of<LentoDeckModel>(context).cards[index],
              //         child: const LentoCard())))
              child: PageView.builder(
                  itemBuilder: (context, index) => LentoCard(
                      lentoCard:
                          Provider.of<LentoDeckModel>(context).cards[index])))
        ],
      ),
    )));
  }
}
