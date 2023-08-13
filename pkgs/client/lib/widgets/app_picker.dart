import 'dart:io';

import 'package:file_picker/file_picker.dart';

Future<File?> showAppPicker() async {
  if (Platform.isMacOS) {
    var result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      initialDirectory: '/Applications/',
      allowedExtensions: ['app'],
    );
    return result != null ? File(result.files.single.path!) : null;
  } else {
    throw 'Platform not yet supported by AppPicker!';
  }
}
