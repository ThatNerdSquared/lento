import 'dart:io';
import 'package:logging/logging.dart';
import 'package:socks5_proxy/enums/command_reply_code.dart';
import 'package:socks5_proxy/socks_server.dart';
import '../config.dart';
import '../notifs.dart';
import 'browser_compat_check.dart';
import 'platform_proxy_settings.dart';

class BlockedWebsiteItem {
  final bool isRestrictedAccess;
  final String? popupMessage;
  DateTime? lastChallenged;
  bool canBypassRestriction;

  BlockedWebsiteItem(
      {required this.isRestrictedAccess,
      required this.popupMessage,
      this.lastChallenged,
      this.canBypassRestriction = false});

  /// Used to avoid showing popups repeatedly, which happens when
  /// a blocked site sends multiple requests from loading assets, etc
  bool wasRecentlyChallenged() {
    return lastChallenged != null &&
        DateTime.now().difference(lastChallenged!).inSeconds < 3;
  }

  void setChallenged() {
    lastChallenged = DateTime.now();
  }
}

class ProxyController {
  final log = Logger('Class: ProxyController');
  late SocksServer socksServer;
  late ServerSocket proxy;
  Map<Uri, BlockedWebsiteItem> blockedSites = {};

  ProxyController(Map websites) {
    blockedSites = websites.map((key, value) {
      return MapEntry(
          Uri(host: key),
          BlockedWebsiteItem(
            isRestrictedAccess: value['isRestrictedAccess'],
            popupMessage: value['popupMessage'],
          ));
    });
  }

  Future<void> setup() async {
    socksServer = SocksServer();
    socksServer.connections.listen(handler).onError(print);
    await socksServer.bind(InternetAddress.loopbackIPv4, 0);
    proxy = socksServer.proxies.values.elementAt(0);
    final proxyPort = proxy.port;
    getPlatformProxySettings().enableProxy(proxyPort);
    ensureFirefoxCompat();
    log.info('Proxying at ${proxy.address}:$proxyPort');
  }

  void handler(Connection connection) async {
    final detectedSiteUrl = detectBlockedSite(connection.desiredAddress.host);
    if (detectedSiteUrl == null) {
      return await connection.forward();
    }
    final detectedSite = blockedSites[detectedSiteUrl]!;

    if (!detectedSite.isRestrictedAccess) {
      log.info('WEBSITE: BLOCKED: $detectedSiteUrl blocked');
      if (!detectedSite.wasRecentlyChallenged()) {
        showBlockedItemPopup(
          blockedItemName: detectedSiteUrl.host,
          popupMsg: detectedSite.popupMessage,
        );
      }
      detectedSite.setChallenged();
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

  /// as much as i hate needing to use this function to check if a given url
  /// is the same as a blocked one, it's the only way i can think of to do it.
  /// there's not really a good way to cut out subdomains, especially
  /// considering the different types of TLDs, etc.
  ///
  /// besides, i think this also works if you want to block a specific subdomain?
  Uri? detectBlockedSite(String rawURL) {
    for (final site in blockedSites.keys) {
      if (rawURL.contains(site.host)) {
        return site;
      }
    }
    return null;
  }

  Future<void> challengeRestrictedAccess(
    Uri detectedSiteUrl,
    BlockedWebsiteItem detectedSite,
    Connection connection,
  ) async {
    if (detectedSite.wasRecentlyChallenged() ||
        !promptUserToUnblock(detectedSiteUrl.host)) {
      log.info('WEBSITE: RESTRICTED: $detectedSiteUrl blocked');
      detectedSite.lastChallenged = DateTime.now();
      return await connection.reject(CommandReplyCode.connectionDenied);
    }
    log.info('WEBSITE: RESTRICTED: extended usage for $detectedSiteUrl');
    detectedSite.setChallenged();
    detectedSite.canBypassRestriction = true;
    return await connection.forward();
  }

  void cleanup() async {
    getPlatformProxySettings().disableProxy();
    proxy.close();
    log.info('Proxy takedown complete.');
  }
}
