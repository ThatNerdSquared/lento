import 'dart:async';
import 'dart:io';
import 'package:logging/logging.dart';
import 'package:shelf/shelf.dart';
import 'package:shelf/shelf_io.dart';
import 'package:shelf_proxy/shelf_proxy.dart';
import '../config.dart';

class ProxyController {
  final log = Logger('Class: ProxyController');
  late HttpServer server;
  Map blockedSitesMap = {};

  ProxyController(this.blockedSitesMap);

  void setup() async {
    server = await serve(handler, 'localhost', 0);
    var proxyPort = server.port.toString();
    await Process.run(
        'networksetup', ['-setwebproxy', 'wi-fi', 'localhost', proxyPort]);
    await Process.run('networksetup',
        ['-setsecurewebproxy', 'wi-fi', 'localhost', proxyPort]);
    log.info('Proxying at http://${server.address.host}:$proxyPort');
  }

  FutureOr<Response> handler(Request request) async {
    var url = request.url.toString();
    print('request.url.path: ${request.url.path}');
    if (blockedSitesMap.containsKey(url)) {
      log.info('WEBSITE: Blocked website $url detected');
      if (!blockedSitesMap[url]['isSoftBlock']) {
        log.info('WEBSITE: HARD blocked website $url detected');
        var popupMessage = blockedSitesMap[url]['popupMessage'];
        await Process.run(notifHelperPath, [
          'popup',
          '$url hard-blocked',
          'Lento has hard-blocked the website "$url" during your work session. Your message: $popupMessage'
        ]);
        log.info('WEBSITE: HARD: $url blocked');
        return Response.forbidden(null);
      } else {
        log.info('WEBSITE: SOFT blocked website $url detected');
        if (DateTime.now()
                .difference(blockedSitesMap[url]['lastOpened'])
                .inMinutes >
            15) {
          String isAllowedString = (await Process.run(notifHelperPath, [
            'popup',
            '$url soft-blocked',
            'Lento has soft-blocked the website "$url" during your work session. Does usage need to be extended by 15 minutes?'
          ]))
              .stdout();
          var isAllowed = isAllowedString == 'flutter: AlertButton.yesButton';
          blockedSitesMap[url]['lastOpened'] = DateTime.now();
          blockedSitesMap[url]['isAllowed'] = isAllowed;
          if (isAllowed) {
            log.info('WEBSITE: SOFT: extended usage for $url');
            return proxyHandler(request.url.path)(request);
          } else {
            log.info('WEBSITE: SOFT: $url blocked');
            return Response.forbidden(null);
          }
        } else {
          return Response.ok(null);
        }
      }
    } else {
      return proxyHandler(request.url.path)(request);
    }
  }

  void cleanup() {
    server.close();
  }
}
