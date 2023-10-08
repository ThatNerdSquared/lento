import 'dart:io';

import 'package:meta/meta.dart';

@immutable
class ProcessInfo {
  final String name;
  final int pid;

  const ProcessInfo({
    required this.name,
    required this.pid,
  });
}

PlatformProcessManager getPlatformProcessManager() =>
    switch (Platform.operatingSystem) {
      'macos' => MacosProcessManager(),
      _ => throw UnimplementedError(
          'Platform process manager for ${Platform.operatingSystem} not yet supported!',
        )
    };

abstract class PlatformProcessManager {
  List<String> rawProcesses();

  ProcessInfo processInfo(String rawProcess);

  void killProcess(ProcessInfo process);

  void restartProcess(ProcessInfo process);
}

class MacosProcessManager extends PlatformProcessManager {
  @override
  List<String> rawProcesses() {
    final processes = (Process.runSync('ps', [
      '-acxo',
      'pid,comm',
    ])).stdout.split('\n');
    processes.removeAt(0);
    processes.removeAt(processes.length - 1);
    return processes;
  }

  @override
  ProcessInfo processInfo(String rawProcess) {
    final trimmedLine = rawProcess.trim();
    var firstSpace = trimmedLine.indexOf(' ');
    return ProcessInfo(
      name: trimmedLine.substring(firstSpace + 1, trimmedLine.length),
      pid: int.parse(trimmedLine.substring(0, firstSpace)),
    );
  }

  @override
  void killProcess(ProcessInfo process) {
    Process.runSync('kill', [process.pid.toString()]);
  }

  @override
  void restartProcess(ProcessInfo process) {
    Process.run('open', ['-a', process.name]);
  }
}
