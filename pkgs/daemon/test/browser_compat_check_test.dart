import 'package:daemon/blockers/browser_compat_check.dart';
import 'package:test/test.dart';

void main() {
  final payload = [
    '// DO NOT REMOVE - AUTOMATICALLY ADDED BY LENTO TO ENSURE BLOCK COMPATABILITY',
    'user_pref("network.proxy.default_pac_script_socks_version", 5);'
  ].join('\n');

  test('correctly add payload to blank user.js file', () {
    expect(addPayloadToUserJS([]), payload);
  });

  test('correctly add payload to existing user.js file', () {
    expect(
      addPayloadToUserJS(['console.log(var)']),
      'console.log(var)\n$payload',
    );
  });

  group('verify inserted socks version is 5', () {
    test('verify version is 5 with new user.js', () {
      expect(addPayloadToUserJS([]), endsWith('5);'));
    });

    test('verify version is 5 with existing user.js', () {
      expect(addPayloadToUserJS(['console.log(var)']), endsWith('5);'));
    });
  });
}
