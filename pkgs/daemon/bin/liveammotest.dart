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
    'banners': {
      '6667e5cf-8cd2-499e-9414-ce6531aaf3d0': {
        'title': 'banner1 title',
        'message': 'banner1 msg',
        'triggerTimes': [30, 60],
      },
      '38e03105-7723-4df3-b635-e0cd54571a9d': {
        'title': 'banner2 title',
        'message': 'banner2 msg',
        'triggerTimes': [50],
      }
    },
    'blockDuration': 70,
  };

  print(cardInfo.toString());
  socket.write(json.encode(cardInfo));
}
