import 'dart:io';
import 'dart:typed_data';

import 'package:favicon/favicon.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:http/http.dart' as http;
import 'package:mime/mime.dart';
import 'package:path/path.dart' as p;

import '../config.dart';

class IconManager {
  final Map<String, Widget> _iconsCache = {};

  IconManager() {
    var iconDir = Directory(Config().iconDirPath);
    if (!iconDir.existsSync()) {
      iconDir.createSync();
    } else {
      for (final item in iconDir.listSync()) {
        final fileType = lookupMimeType(item.path);
        // TODO: log warning when we cannot read filetype
        if (fileType == null) continue;
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
    var favicon = await FaviconFinder.getBest(url);
    final response = await http.get(Uri.parse(favicon!.url));
    final iconExt = favicon.url.substring(favicon.url.lastIndexOf('.'));
    final imageFile = File(p.join(Config().iconDirPath, '$iconId$iconExt'));
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
      throw UnimplementedError('This feature hasn\'t been built for apps yet!');
    }
  }
}
