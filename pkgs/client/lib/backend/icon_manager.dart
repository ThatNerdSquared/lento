import 'dart:io';
import 'dart:typed_data';

import 'package:favicon/favicon.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:http/http.dart' as http;
import 'package:logging/logging.dart';
import 'package:mime/mime.dart';
import 'package:path/path.dart' as p;
import 'package:plist_parser/plist_parser.dart';

import '../config.dart';

final _logger = Logger('IconManager');

IconManager getIconManager() => switch (Platform.operatingSystem) {
      'macos' => MacosIconManager(),
      'windows' => WindowsIconManager(),
      _ => throw UnimplementedError(
          'Icon manager for ${Platform.operatingSystem} not yet supported!',
        )
    };

abstract class IconManager {
  final Map<String, Widget> _iconsCache = {};

  IconManager() {
    if (!Config.iconDir.existsSync()) {
      Config.iconDir.createSync();
    } else {
      for (final item in Config.iconDir.listSync()) {
        final fileType = lookupMimeType(item.path);
        if (fileType == null) {
          _logger.warning('Could not read filetype for file "${item.path}"');
          continue;
        }
        if (fileType.startsWith('image/')) {
          _iconsCache[p.basenameWithoutExtension(item.path)] = _bytesToImage(
              ext: p.extension(item.path),
              bytes: File(item.path).readAsBytesSync());
        }
      }
    }
  }

  Widget _bytesToImage({required String ext, required Uint8List bytes}) =>
      switch (ext) {
        '.svg' => SvgPicture.memory(
            bytes,
            width: Config.blockItemIconSize,
            height: Config.blockItemIconSize,
          ),
        _ => Image.memory(
            bytes,
            width: Config.blockItemIconSize,
            height: Config.blockItemIconSize,
          )
      };

  Future<Widget> loadWebsiteIcon(String iconId, String url) async {
    if (_iconsCache.containsKey(iconId)) return _iconsCache[iconId]!;
    final favicon = await FaviconFinder.getBest(url);
    final response = await http.get(Uri.parse(favicon!.url));
    final iconExt = favicon.url.substring(favicon.url.lastIndexOf('.'));
    final imageFile = File(p.join(Config.iconDir.path, '$iconId$iconExt'));
    await imageFile.writeAsBytes(response.bodyBytes);
    final icon = _bytesToImage(ext: iconExt, bytes: response.bodyBytes);
    _iconsCache[iconId] = icon;
    return icon;
  }

  Future<Widget> loadAppIcon(
    String iconId,
    String sourcePath,
  ) async {
    if (_iconsCache.containsKey(iconId)) {
      return _iconsCache[iconId]!;
    } else {
      return _loadPlatformAppIcon(iconId, sourcePath);
    }
  }

  Future<Widget> _loadPlatformAppIcon(String iconId, String sourcePath);
}

class MacosIconManager extends IconManager {
  @override
  Future<Widget> _loadPlatformAppIcon(String iconId, String sourcePath) async {
    final plistPath = p.join(sourcePath, 'Contents', 'Info.plist');
    final plist = await PlistParser().parseFile(plistPath);
    const iconExt = '.icns';
    final rawIconName = plist['CFBundleIconFile'].toString();
    final dotIndex = rawIconName.lastIndexOf('.');
    final iconName =
        dotIndex == -1 || rawIconName.substring(dotIndex) != iconExt
            ? rawIconName + iconExt
            : rawIconName;
    final iconPath = p.join(sourcePath, 'Contents', 'Resources', iconName);
    final iconBytes = await File(iconPath).readAsBytes();
    File(p.join(Config.iconDir.path, '$iconId$iconExt'))
        .writeAsBytesSync(iconBytes);
    return _bytesToImage(ext: iconExt, bytes: iconBytes);
  }
}

class WindowsIconManager extends IconManager {
  @override
  Future<Widget> _loadPlatformAppIcon(String iconId, String sourcePath) {
    throw UnimplementedError(
        'WindowsIconManager does not yet support app icons!');
  }
}
