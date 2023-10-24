import 'dart:convert';
import 'dart:io';

final exampleDaemonInput = File('../../docs/example-daemon-input.json');

void main(List<String> args) async {
  final port = args[0];
  final socket = await Socket.connect('localhost', int.parse(port));

  socket.listen((data) {
    final message = String.fromCharCodes(data);
    print(message);
  }, onError: (error) {
    print(error);
    socket.destroy();
  }, onDone: () {
    print('Data sent to daemon');
    socket.destroy();
  });

  final cardInfo = jsonDecode(exampleDaemonInput.readAsStringSync());
  print(cardInfo.toString());
  socket.write(json.encode(cardInfo));
}
