import 'package:daemon/blockers/platform_proxy_settings.dart';
import 'package:daemon/blockers/proxy.dart';
import 'package:daemon/notifs.dart';
import 'package:mockito/annotations.dart';
import 'package:test/test.dart';

@GenerateNiceMocks([
  MockSpec<NotifManager>(),
  MockSpec<PlatformProxySettings>(),
])
import 'url_detection_test.mocks.dart';

void main() {
  final mockNotifManager = MockNotifManager();
  final mockProxySettings = MockPlatformProxySettings();

  test('correctly detect domain with single-part TLD', () {
    final proxy = LentoProxy(websites: {
      'example.com': {
        'isRestrictedAccess': false,
      }
    }, proxySettings: mockProxySettings, notifManager: mockNotifManager);
    final res = proxy.detectBlockedSite('https://example.com');
    final resWithSubdomain = proxy.detectBlockedSite(
      'http://something.example.com',
    );
    expect(res, TypeMatcher<Uri>());
    expect(resWithSubdomain, TypeMatcher<Uri>());
  });

  test('correctly detect domain with multi-part TLD', () {
    final proxy = LentoProxy(websites: {
      'example.co.uk': {
        'isRestrictedAccess': false,
      }
    }, proxySettings: mockProxySettings, notifManager: mockNotifManager);
    final res = proxy.detectBlockedSite('http://example.co.uk');
    final resWithSubdomain = proxy.detectBlockedSite(
      'https://something.example.co.uk',
    );
    expect(res, TypeMatcher<Uri>());
    expect(resWithSubdomain, TypeMatcher<Uri>());
  });

  test('correctly detect subdomain only', () {
    final proxy = LentoProxy(websites: {
      'something.example.com': {
        'isRestrictedAccess': false,
      }
    }, proxySettings: mockProxySettings, notifManager: mockNotifManager);
    final resWithSubdomain = proxy.detectBlockedSite(
      'http://something.example.com',
    );
    final res = proxy.detectBlockedSite('https://example.com');
    expect(resWithSubdomain, TypeMatcher<Uri>());
    expect(res, isNull);
  });

  test('correctly detect URL paths', () {
    final proxy = LentoProxy(websites: {
      'something.example.com': {
        'isRestrictedAccess': false,
      },
      'something.co.uk': {
        'isRestrictedAccess': false,
      }
    }, proxySettings: mockProxySettings, notifManager: mockNotifManager);
    final res = proxy.detectBlockedSite(
      'http://something.example.com/test',
    );
    final resMultiPartTLD = proxy.detectBlockedSite(
      'http://something.co.uk/test',
    );
    expect(res, TypeMatcher<Uri>());
    expect(resMultiPartTLD, TypeMatcher<Uri>());
  });
}
