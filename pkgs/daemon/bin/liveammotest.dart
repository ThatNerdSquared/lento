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
      'Spotify': {
        'isRestrictedAccess': false,
        'isAllowed': false,
        'popupMessage': 'spotify-popup'
      },
      'thonny': {
        'isRestrictedAccess': true,
        'isAllowed': false,
        'popupMessage': 'thonny-popup'
      },
      'Roblox': {
        'isRestrictedAccess': true,
        'isAllowed': false,
        'popupMessage': 'roblox-popup'
      }
    },
    'websites': {
      'example.com': {
        'isRestrictedAccess': false,
        'isAllowed': false,
        'popupMessage': 'cheese',
        'lastOpened': '2023-09-01 21:18:54.579347'
      },
      'www.charlie.com': {
        'isRestrictedAccess': true,
        'isAllowed': false,
        'popupMessage': 'lardmamn',
        'lastOpened': '2023-09-01 21:18:54.579347'
      },
      'neverssl.com': {
        'isRestrictedAccess': false,
        'isAllowed': false,
        'popupMessage': 'hehehehehehe',
        'lastOpened': '2023-09-01 21:18:54.579347'
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
