import 'package:daemon/blockers/proxy_controller.dart';
import 'package:test/test.dart';

void main() {
  test('correctly detect domain with single-part TLD', () {
    final proxy = ProxyController({
      'example.com': {
        'isRestrictedAccess': false,
      }
    });
    final res = proxy.detectBlockedSite('https://example.com');
    final resWithSubdomain = proxy.detectBlockedSite(
      'http://something.example.com',
    );
    expect(res, TypeMatcher<Uri>());
    expect(resWithSubdomain, TypeMatcher<Uri>());
  });

  test('correctly detect domain with multi-part TLD', () {
    final proxy = ProxyController({
      'example.co.uk': {
        'isRestrictedAccess': false,
      }
    });
    final res = proxy.detectBlockedSite('http://example.co.uk');
    final resWithSubdomain = proxy.detectBlockedSite(
      'https://something.example.co.uk',
    );
    expect(res, TypeMatcher<Uri>());
    expect(resWithSubdomain, TypeMatcher<Uri>());
  });

  test('correctly detect subdomain only', () {
    final proxy = ProxyController({
      'something.example.com': {
        'isRestrictedAccess': false,
      }
    });
    final resWithSubdomain = proxy.detectBlockedSite(
      'http://something.example.com',
    );
    final res = proxy.detectBlockedSite('https://example.com');
    expect(resWithSubdomain, TypeMatcher<Uri>());
    expect(res, isNull);
  });

  test('correctly detect paths', () {
    final proxy = ProxyController({
      'something.example.com': {
        'isRestrictedAccess': false,
      },
      'something.co.uk': {
        'isRestrictedAccess': false,
      }
    });
    final res = proxy.detectBlockedSite(
      'http://something.example.com/test',
    );
    expect(res, TypeMatcher<Uri>());
  });
}
