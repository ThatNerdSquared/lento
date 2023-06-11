import 'package:flutter/material.dart';

import 'card.dart';
import 'config.dart';

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
          scaffoldBackgroundColor: lentoLightColorScheme.surface,
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
    return const Scaffold(
      body: Center(
        child: LentoCard(),
      ),
    );
  }
}
