import 'dart:io';
import 'package:logging/logging.dart';
import '../config.dart';

class ProxyController {
  final log = Logger('Class: ProxyController');
  late HttpServer server;
  Map blockedSites = {};

  ProxyController(this.blockedSites);

  void setup() async {
    server = await HttpServer.bind('localhost', 0);
    var proxyPort = server.port.toString();
    Process.run(
        'networksetup', ['-setwebproxy', 'wi-fi', 'localhost', proxyPort]);
    Process.run('networksetup',
        ['-setsecurewebproxy', 'wi-fi', 'localhost', proxyPort]);
    log.info('Proxying at http://${server.address.host}:$proxyPort');
    
    server.listen((final request) {
      var localhost = Uri(path: 'localhost');

      if (blockedSites.containsKey(request.uri.toString())) {
        var uri = request.uri.toString();
        log.info('WEBSITE: Blocked website $uri detected');
        var website = blockedSites[uri];
        print('website: $website');

        if (!website['isSoftBlock']) {
          log.info('WEBSITE: HARD blocked website $uri detected');
          var popupMessage = website['popupMessage'];
          Process.run(notifHelperPath, [
            'banner', // change to popup later
            '$uri hard-blocked',
            'Lento has hard-blocked the website "$uri" during your work session. Your message: $popupMessage'
          ]);
          log.info('WEBSITE: HARD: $uri blocked');
          request.response.redirect(localhost);
          log.info('WEBSITE: HARD: $uri killed');
        } else {
          log.info('WEBSITE: SOFT blocked website $uri detected');
          if (website['permClosed'] != true) {
            if (DateTime.now().difference(website['lastOpened']).inSeconds > 15) {
              var isAllowedPopup = Process.runSync(notifHelperPath, [
                'popup',
                '$uri soft-blocked',
                'Lento has soft-blocked the app "$uri" during your work session. Does usage need to be extended by 15 minutes?'
              ]);
              var isAllowedString = isAllowedPopup.stdout.trim();
              var isAllowed = isAllowedString == 'flutter: AlertButton.yesButton';
              print('isAllowed $isAllowed');
              if (isAllowed) {
                log.info('WEBSITE: SOFT: extended usage for $uri');
              } else {
                  log.info('WEBSITE: SOFT: $uri blocked');
                  website['permClosed'] = true;
                  Process.run(notifHelperPath, [
                    'banner',
                    '$uri soft-blocked',
                    'Lento has blocked the website "$uri" for the rest of your work session.'
                  ]);
              }
              website['lastOpened'] = DateTime.now();
              website['isAllowed'] = isAllowed;
            }
          } else {
            Process.run(notifHelperPath, [
                'banner',
                '$uri soft-blocked',
                'Lento has blocked the app "$uri" for the rest of your work session.']);
          }
        }
      }
    });
  }

  void cleanup() {
    server.close();
  }
}
