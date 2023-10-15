import 'dart:io';
import 'package:logging/logging.dart';
import 'package:socks5_proxy/enums/command_reply_code.dart';
import 'package:socks5_proxy/socks_server.dart';
import '../config.dart';
import '../db.dart' as db;
import '../notifs.dart';
import 'browser_compat_check.dart';
import 'platform_proxy_settings.dart';

class LentoProxy {
  final log = Logger('Class: ProxyController');
  late SocksServer socksServer;
  late ServerSocket proxy;
  NotifManager notifManager;
  PlatformProxySettings proxySettings;

  LentoProxy({
    required this.proxySettings,
    required this.notifManager,
  });

  Future<void> setup() async {
    socksServer = SocksServer();
    socksServer.connections.listen(handler).onError(print);
    await socksServer.bind(InternetAddress.loopbackIPv4, 0);
    proxy = socksServer.proxies.values.elementAt(0);
    final proxyPort = proxy.port;
    proxySettings.enableProxy(proxyPort);
    ensureFirefoxCompat();
    log.info('Proxying at ${proxy.address}:$proxyPort');
  }

  void handler(Connection connection) async {
    final detectedSiteUrl =
        db.detectBlockedSite(connection.desiredAddress.host);
    if (detectedSiteUrl == null) {
      return await connection.forward();
    }
    final detectedSite = db.getBlockedSite(detectedSiteUrl);

    if (!detectedSite.isRestrictedAccess) {
      log.info('WEBSITE: BLOCKED: $detectedSiteUrl blocked');
      if (!detectedSite.wasRecentlyChallenged()) {
        notifManager.showBlockedItemPopup(
          blockedItemName: detectedSiteUrl.host,
          popupMsg: detectedSite.popupMessage,
        );
      }
      db.recordSiteChallenge(detectedSite);
      return await connection.reject(CommandReplyCode.connectionDenied);
    }

    log.info(
        'WEBSITE: RESTRICTED: restricted website $detectedSiteUrl detected');
    if (!detectedSite.canBypassRestriction ||
        DateTime.now().difference(detectedSite.lastChallenged!).inMinutes >
            restrictionBypassTTL) {
      return await challengeRestrictedAccess(
        detectedSiteUrl,
        detectedSite,
        connection,
      );
    }
    return await connection.forward();
  }

  Future<void> challengeRestrictedAccess(
    Uri detectedSiteUrl,
    db.BlockedWebsiteItem detectedSite,
    Connection connection,
  ) async {
    if (detectedSite.wasRecentlyChallenged() ||
        !notifManager.promptUserToUnblock(detectedSiteUrl.host)) {
      log.info('WEBSITE: RESTRICTED: $detectedSiteUrl blocked');
      db.recordSiteChallenge(detectedSite);
      return await connection.reject(CommandReplyCode.connectionDenied);
    }
    log.info('WEBSITE: RESTRICTED: extended usage for $detectedSiteUrl');
    db.recordSiteChallenge(detectedSite);
    db.setSiteRestrictionBypass(site: detectedSite, canBypassRestriction: true);
    return await connection.forward();
  }

  void cleanup() async {
    proxySettings.disableProxy();
    proxy.close();
    log.info('Proxy takedown complete.');
  }
}
