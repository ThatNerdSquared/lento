import 'package:daemon/blockers/appblocker.dart';
import 'package:daemon/blockers/platform_process_manager.dart';
import 'package:daemon/notifs.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:test/test.dart';

@GenerateNiceMocks([
  MockSpec<PlatformProcessManager>(),
  MockSpec<NotifManager>(),
])
import 'appblocker_test.mocks.dart';

void main() {
  final mockProcessManager = MockPlatformProcessManager();
  final mockNotifManager = MockNotifManager();

  final fakeRawProcess = 'testrawprocess';
  final fakeProcessInfo = ProcessInfo(name: 'Test', pid: 1234);
  final fakeAppName = 'Test';
  final fakePopupMsg = 'testPopupMsg';
  final fakeApps = {
    fakeAppName: {
      'isRestrictedAccess': false,
      'popupMessage': fakePopupMsg,
    }
  };
  final fakeRestrictedApps = {
    fakeAppName: {
      'isRestrictedAccess': true,
      'popupMessage': fakePopupMsg,
    }
  };

  setUp(() {
    when(mockProcessManager.rawProcesses()).thenReturn([fakeRawProcess]);
    when(mockProcessManager.processInfo(fakeRawProcess))
        .thenReturn(fakeProcessInfo);
  });

  test('blocked app is killed with popup', () {
    final appBlocker = AppBlocker(
      apps: fakeApps,
      processManager: mockProcessManager,
      notifManager: mockNotifManager,
    );
    appBlocker.blockApps();
    verify(mockProcessManager.killProcess(fakeProcessInfo));
    verify(mockNotifManager.showBlockedItemPopup(
        blockedItemName: fakeProcessInfo.name, popupMsg: fakePopupMsg));
  });

  test('restricted app is reopened with approval', () {
    when(mockNotifManager.promptUserToUnblock(fakeAppName)).thenReturn(true);

    final appBlocker = AppBlocker(
      apps: fakeRestrictedApps,
      processManager: mockProcessManager,
      notifManager: mockNotifManager,
    );
    appBlocker.blockApps();

    verify(mockProcessManager.killProcess(fakeProcessInfo));
    verify(mockNotifManager.promptUserToUnblock(fakeAppName));
    verify(mockProcessManager.restartProcess(fakeProcessInfo));
    verifyNever(mockNotifManager.showBlockedItemPopup(
        blockedItemName: fakeProcessInfo.name, popupMsg: fakePopupMsg));
  });

  test('restricted app remains closed if no approval given', () {
    when(mockNotifManager.promptUserToUnblock(fakeAppName)).thenReturn(false);

    final appBlocker = AppBlocker(
      apps: fakeRestrictedApps,
      processManager: mockProcessManager,
      notifManager: mockNotifManager,
    );
    appBlocker.blockApps();

    verify(mockProcessManager.killProcess(fakeProcessInfo));
    verify(mockNotifManager.promptUserToUnblock(fakeAppName));
    verify(mockNotifManager.showBlockedItemPopup(
        blockedItemName: fakeProcessInfo.name, popupMsg: fakePopupMsg));
    verifyNever(mockProcessManager.restartProcess(fakeProcessInfo));
  });

  test('previously allowed restricted app is not affected', () {
    final appBlocker = AppBlocker(
      apps: {
        fakeAppName: {
          'isRestrictedAccess': true,
          'popupMessage': fakePopupMsg,
          'canBypassRestriction': true,
        }
      },
      processManager: mockProcessManager,
      notifManager: mockNotifManager,
    );
    appBlocker.blockApps();

    verifyNever(mockProcessManager.killProcess(fakeProcessInfo));
    verifyNever(mockNotifManager.promptUserToUnblock(fakeAppName));
    verifyNever(mockNotifManager.showBlockedItemPopup(
        blockedItemName: fakeProcessInfo.name, popupMsg: fakePopupMsg));
    verifyNever(mockProcessManager.restartProcess(fakeProcessInfo));
  });
}
