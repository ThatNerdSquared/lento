import 'package:flutter/material.dart';
import 'package:path/path.dart' as p;
import 'package:pret_a_porter/pret_a_porter.dart';

import 'main.dart';

enum TimeSection { hours, minutes, seconds }

enum BlockItemType { website, app }

class Config {
  static const double defaultMarginPercentage = 0.15;

  String get dataFilePath {
    return p.join(
      platformAppSupportDir,
      'lentosettings.json',
    );
  }

  String get iconDirPath {
    return p.join(
      platformAppSupportDir,
      'icons',
    );
  }
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
