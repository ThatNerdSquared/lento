import 'package:flutter/material.dart';

enum TimeSection { hours, minutes, seconds }

class Config {
  static const BorderRadius defaultBorderRadius =
      BorderRadius.all(Radius.circular(20));
  static const double defaultElementSpacing = 15.0;
  static const BoxShadow defaultShadow = BoxShadow(
      color: Color.fromRGBO((0), 0, 0, 0.20),
      offset: Offset(0, 4),
      blurRadius: 20.0);
}

const ColorScheme lentoLightColorScheme = ColorScheme(
  brightness: Brightness.light,
  shadow: Color.fromRGBO((0), 0, 0, 0.20),
  background: Colors.white,
  onBackground: Colors.black,
  primary: Colors.white,
  onPrimary: Colors.black,
  secondary: Color(0xFFE6E6E6),
  onSecondary: Color(0xFF565656),
  surface: Color(0xFFF4F4F4),
  surfaceTint: Color(0x1AC780FF),
  onSurface: Color(0xFF565656),
  tertiary: Color(0xFFC780FF),
  error: Color(0xFFE20C0C),
  onError: Colors.white,
);

CardTheme lentoCardTheme = const CardTheme(
  shape: RoundedRectangleBorder(borderRadius: Config.defaultBorderRadius),
);
