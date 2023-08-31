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
  Map blockedSites = {};

  ProxyController(this.blockedSites);

  void setup() async {
    server = await serve(
      handler,
      'localhost',
      0,
      securityContext: SecurityContext.defaultContext,
    );
    var proxyPort = server.port.toString();
    await Process.run(
        'networksetup', ['-setwebproxy', 'wi-fi', 'localhost', proxyPort]);
    await Process.run('networksetup',
        ['-setsecurewebproxy', 'wi-fi', 'localhost', proxyPort]);
    log.info('Proxying at http://${server.address.host}:$proxyPort');
  }

  FutureOr<Response> handler(Request request) async {
    final siteUrl = request.requestedUri.host;
    print('~~~~~~');
    print(request.requestedUri);
    print(siteUrl);
    print('~~~~~~');

    if (blockedSites.containsKey(siteUrl)) {
      log.info('WEBSITE: Blocked website $siteUrl detected');
      final website = blockedSites[siteUrl];
      print('website: $website');

      if (!website['isSoftBlock']) {
        log.info('WEBSITE: HARD blocked website $siteUrl detected');
        final popupMessage = website['popupMessage'];
        Process.run(notifHelperPath, [
          'banner', // change to popup later
          '$siteUrl hard-blocked',
          'Lento has hard-blocked the website "$siteUrl" during your work session.\n$popupMessage'
        ]);
        log.info('WEBSITE: HARD: $siteUrl blocked');
        return Response.forbidden(null);
      } else {
        log.info('WEBSITE: SOFT blocked website $siteUrl detected');
        if (website['permClosed'] != true) {
          if (DateTime.now().difference(website['lastOpened']).inSeconds > 15) {
            final popupResponse = Process.runSync(notifHelperPath, [
              'popup',
              '$siteUrl soft-blocked',
              'Lento has soft-blocked the app "$siteUrl" during your work session. Does usage need to be extended by 15 minutes?'
            ]);
            final isAllowed = popupResponse.stdout.toString().trim() ==
                'flutter: AlertButton.yesButton';
            print('isAllowed $isAllowed');
            website['lastOpened'] = DateTime.now();
            website['isAllowed'] = isAllowed;
            if (isAllowed) {
              log.info('WEBSITE: SOFT: extended usage for $siteUrl');
              return proxyHandler(request.requestedUri)(request);
            } else {
              log.info('WEBSITE: SOFT: $siteUrl blocked');
              website['permClosed'] = true;
              Process.run(notifHelperPath, [
                'banner',
                '$siteUrl soft-blocked',
                'Lento has blocked the website "$siteUrl" for the rest of your work session.'
              ]);
              return Response.forbidden(null);
            }
          }
          print('weird if conditional you got there mate');
          return Response.forbidden(null);
        } else {
          Process.run(notifHelperPath, [
            'banner',
            '$siteUrl soft-blocked',
            'Lento has blocked the app "$siteUrl" for the rest of your work session.'
          ]);
          return Response.forbidden(null);
        }
      }
    } else {
      return proxyHandler(request.requestedUri)(request);
    }
  }

  void cleanup() async {
    server.close();
    await Process.run('networksetup', ['-setwebproxystate', 'wi-fi', 'off']);
    await Process.run(
        'networksetup', ['-setsecurewebproxystate', 'wi-fi', 'off']);
  }
}
