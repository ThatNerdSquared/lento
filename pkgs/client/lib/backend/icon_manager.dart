import 'dart:io';

import 'package:favicon/favicon.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:mime/mime.dart';
import 'package:path/path.dart';

import '../config.dart';

class IconManager {
  final Map<String, ImageIcon> _iconsCache = {};

  IconManager() {
    var iconDir = Directory(Config().iconDirPath);
    if (!iconDir.existsSync()) {
      iconDir.createSync();
    } else {
      for (final item in iconDir.listSync()) {
        if (lookupMimeType(item.path)!.startsWith('image/')) {
          _iconsCache[basenameWithoutExtension(item.path)] =
              ImageIcon(FileImage(File(item.path)));
        }
      }
    }
  }

  Future<ImageIcon> loadWebsiteIcon(String iconId, String url) async {
    if (_iconsCache.containsKey(iconId)) return _iconsCache[iconId]!;
    var favicon = await FaviconFinder.getBest(url);
    final response = await http.get(Uri.parse(favicon!.url));
    final imageFile = File(join(Config().iconDirPath, iconId));
    await imageFile.writeAsBytes(response.bodyBytes);
    final icon = ImageIcon(MemoryImage(response.bodyBytes));
    _iconsCache[iconId] = icon;
    return icon;
  }

  // Future<ImageIcon> loadAppIcon(
  dynamic loadAppIcon(
    String iconId,
    String sourcePath,
  ) async {
    if (_iconsCache.containsKey(iconId)) {
      return _iconsCache[iconId]!;
    } else {
      // ignore: avoid_print
      print('getappicon');
      return null;
    }
  }
}
