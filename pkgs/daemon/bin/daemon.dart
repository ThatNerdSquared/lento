import 'package:daemon/daemon.dart';
import 'package:logging/logging.dart';

void main(List<String> args) {
  final devMode = args.isNotEmpty && args[0] == '--devmode';
  Logger.root.level = Level.ALL; // defaults to Level.INFO
  Logger.root.onRecord.listen((record) {
    print('${record.level.name}: ${record.time}: ${record.message}');
  });
  LentoDaemon(devMode: devMode).entry();
}
