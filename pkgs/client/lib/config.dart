import 'dart:io';

import 'package:flutter/material.dart';
import 'package:path/path.dart' as p;
import 'package:pret_a_porter/pret_a_porter.dart';

import 'main.dart';

enum TimeSection { hours, minutes, seconds }

enum BlockItemType { website, app }

enum AppTheme { light, dark, system }

class Config {
  Config._();
  static const double defaultMarginPercentage = 0.15;
  static const double blockItemIconSize = 32.0;
  static String get dataFilePath {
    return p.join(
      platformAppSupportDir,
      'lentosettings.json',
    );
  }

  static String get homeFolder{
    final envVars = Platform.environment;
    return envVars['HOME']!;
  }

  static Directory get iconDir {
    return Directory(p.join(
      platformAppSupportDir,
      'icons',
    ));
  }

  static const defaultSliverPadding = SliverPadding(
    padding: EdgeInsets.only(
      top: PretConfig.defaultElementSpacing,
    ),
  );
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
  shape: RoundedRectangleBorder(borderRadius: PretConfig.defaultBorderRadius),
);

TextTheme lentoTextTheme = const TextTheme(
  displayLarge: TextStyle(
    color: Colors.black,
    fontSize: 48,
    fontWeight: FontWeight.w600,
  ),
  displayMedium: TextStyle(
    color: Colors.black,
    fontSize: 36,
    fontWeight: FontWeight.w600,
  ),
  displaySmall: TextStyle(fontSize: 24, fontWeight: FontWeight.w500),
  labelLarge: TextStyle(fontSize: 18, fontWeight: FontWeight.w500),
  labelMedium: TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
  labelSmall: TextStyle(
    fontSize: 14,
    fontWeight: FontWeight.w500,
    letterSpacing: 0.1,
  ),
  bodyMedium: TextStyle(fontSize: 17, fontWeight: FontWeight.w400),
);
