import 'dart:io';
import 'package:logging/logging.dart';
import 'package:socks5_proxy/enums/command_reply_code.dart';
import 'package:socks5_proxy/socks_server.dart';
import '../config.dart';
import '../url_utils.dart';
import 'browser_compat_check.dart';

class ProxyController {
  final log = Logger('Class: ProxyController');
  late SocksServer socksServer;
  late ServerSocket proxy;
  Map blockedSites = {};

  ProxyController(this.blockedSites);

  void setup() async {
    socksServer = SocksServer();
    socksServer.connections.listen(handler).onError(print);
    await socksServer.bind(InternetAddress.loopbackIPv4, 0);
    proxy = socksServer.proxies.values.elementAt(0);
    final proxyPort = proxy.port.toString();
    await Process.run(
      'networksetup',
      ['-setsocksfirewallproxy', 'wi-fi', 'localhost', proxyPort],
    );
    ensureFirefoxCompat();
    log.info('Proxying at ${proxy.address}:$proxyPort');
  }

  void handler(Connection connection) async {
    // final siteUrl = request.requestedUri.host;
    final siteUrl = getDomainFromHost(connection.desiredAddress.host);
    print('&&^&&^&^&^^&^&^&^&&^&&^&^&^&^&^&^&^&^&^^&^&');
    print('&&^&&^&^&^^&^&^&^&&^&&^&^&^&^&^&^&^&^&^^&^&');
    print(siteUrl);
    print(blockedSites);
    print('&&^&&^&^&^^&^&^&^&&^&&^&^&^&^&^&^&^&^&^^&^&');
    print('&&^&&^&^&^^&^&^&^&&^&&^&^&^&^&^&^&^&^&^^&^&');

    if (!blockedSites.containsKey(siteUrl)) {
      return await connection.forward();
    }

    log.info('WEBSITE: Blocked website $siteUrl detected');
    final website = blockedSites[siteUrl];
    print('website: $website');

    if (!website['isSoftBlock']) {
      log.info('WEBSITE: HARD blocked website $siteUrl detected');
      final popupMessage = website['popupMessage'];
      Process.run(notifHelperPath, [
        'popup',
        '$siteUrl hard-blocked',
        'Lento has hard-blocked the website "$siteUrl" during your work session.\n$popupMessage'
      ]);
      log.info('WEBSITE: HARD: $siteUrl blocked');
      return await connection.reject(CommandReplyCode.connectionDenied);
    }

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
          await connection.forward();
        } else {
          log.info('WEBSITE: SOFT: $siteUrl blocked');
          website['permClosed'] = true;
          Process.run(notifHelperPath, [
            'banner',
            '$siteUrl soft-blocked',
            'Lento has blocked the website "$siteUrl" for the rest of your work session.'
          ]);
          await connection.reject(CommandReplyCode.connectionDenied);
        }
      }
      await connection.reject(CommandReplyCode.connectionDenied);
    } else {
      Process.run(notifHelperPath, [
        'banner',
        '$siteUrl soft-blocked',
        'Lento has blocked the app "$siteUrl" for the rest of your work session.'
      ]);
      await connection.reject(CommandReplyCode.connectionDenied);
    }
  }

  void cleanup() async {
    proxy.close();
    print('sheesh');
    await Process.run(
      'networksetup',
      ['-setsocksfirewallproxystate', 'wi-fi', 'off'],
    );
  }
}
