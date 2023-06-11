import 'package:flutter/material.dart';

class Config {
  static const double defaultBlurRadius = 20.0;
  static const double defaultBorderRadius = 40.0;
  static const double defaultElementSpacing = 15.0;
  static const Offset defaultShadowOffset = Offset(0, 4);
}

const lentoLightColorScheme = ColorScheme(
  brightness: Brightness.light,
  shadow: Color.fromRGBO((0), 0, 0, 0.25),
  // background: Colors.white,
  background: Color(0xFFF5F5F5),
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

CardTheme lentoCardTheme = CardTheme(
  shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(Config.defaultBorderRadius)),
);
