import "dart:io";
import 'package:lento/daemon_config.dart';

 Future<void> _checkForDB() async {
    final DB = File(await dbFilePath);
    final doesFileExist = await DB.exists();
    if (!doesFileExist) {
      DB.create();
    }
  }