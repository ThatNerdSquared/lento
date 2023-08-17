import 'dart:io';
import '../config.dart';

 Future<void> checkForDB() async {
    final db = File(dbFilePath);
    final doesFileExist = await db.exists();
    if (!doesFileExist) {
      db.create();
    }
  }