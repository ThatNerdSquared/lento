import 'dart:io';

import 'package:common/common.dart';
import 'package:daemon/blockers/appblocker.dart';
import 'package:daemon/db.dart' as db;
import 'package:daemon/notifs.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:path/path.dart' as p;
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
    final tempDB =
        File(p.join(Directory.systemTemp.createTempSync().path, 'lento.db'));
    db.init(path: tempDB.path);
  });

  tearDown(db.reset);

  test('blocked app is killed with popup', () {
    db.saveAppData(fakeApps);
    final appBlocker = AppBlocker(
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
    db.saveAppData(fakeRestrictedApps);

    final appBlocker = AppBlocker(
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
    db.saveAppData(fakeRestrictedApps);

    final appBlocker = AppBlocker(
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
    db.saveAppData({
      fakeAppName: {
        'isRestrictedAccess': true,
        'popupMessage': fakePopupMsg,
        'canBypassRestriction': true,
      }
    });
    final appBlocker = AppBlocker(
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
