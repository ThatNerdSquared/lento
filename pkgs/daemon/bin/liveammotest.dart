import 'dart:convert';
import 'dart:io';

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
    // client behaviour when closed from server
    print('Data sent to daemon'); // destroys client socket and server socket
    socket.destroy();
  });

  final cardInfo = {
    'apps': {
      'Spotify': {'isRestrictedAccess': false, 'popupMessage': 'spotify-popup'},
      'thonny': {'isRestrictedAccess': true, 'popupMessage': 'thonny-popup'},
      'Roblox': {'isRestrictedAccess': true, 'popupMessage': 'roblox-popup'}
    },
    'websites': {
      'example.com': {
        'isRestrictedAccess': false,
        'popupMessage': 'cheese',
      },
      'www.charlie.com': {
        'isRestrictedAccess': true,
        'popupMessage': 'lardmamn',
      },
      'neverssl.com': {
        'isRestrictedAccess': false,
        'popupMessage': 'hehehehehehe',
      }
    },
    'bannerText': [
      {'oppenheimer': 'david'},
      {'charlie': '[censored]'}
    ],
    'blockDuration': 70,
    'bannerTriggerTimeIntervals': [30, 60],
  };

  print(cardInfo.toString());
  socket.write(json.encode(cardInfo));
}
