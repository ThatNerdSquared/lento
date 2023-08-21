import 'dart:io';

import 'package:favicon/favicon.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:mime/mime.dart';
import 'package:path/path.dart';

import '../config.dart';

class IconManager {
  Map<String, ImageIcon> iconsStore = {};

  IconManager() {
    var iconDir = Directory(Config().iconDirPath);
    if (!iconDir.existsSync()) {
      iconDir.createSync();
    } else {
      for (final item in iconDir.listSync()) {
        if (lookupMimeType(item.path)!.startsWith('image/')) {
          iconsStore[basenameWithoutExtension(item.path)] =
              ImageIcon(FileImage(File(item.path)));
        }
      }
    }
  }

  Future<ImageIcon> loadIcon(
    String iconId,
    BlockItemType blockItemType,
    String sourcePath,
  ) async {
    if (iconsStore.containsKey(iconId)) {
      return iconsStore[iconId]!;
    } else {
      switch (blockItemType) {
        case BlockItemType.app:
          return _extractAppIcon();
        case BlockItemType.website:
          return await _extractWebsiteIcon(iconId, sourcePath);
      }
    }
  }

  dynamic _extractAppIcon() {
    // ignore: avoid_print
    print('getappicon');
  }

  dynamic _extractWebsiteIcon(String iconId, String url) async {
    var favicon = await FaviconFinder.getBest(url);
    final response = await http.get(Uri.parse(favicon!.url));
    final imageFile = File(join(Config().iconDirPath, iconId));
    await imageFile.writeAsBytes(response.bodyBytes);
    final icon = ImageIcon(MemoryImage(response.bodyBytes));
    iconsStore[iconId] = icon;
    return icon;
  }
}
