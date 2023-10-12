import 'dart:io';

import 'package:clock/clock.dart';
import 'package:daemon/db.dart' as db;
import 'package:daemon/notifs.dart';
import 'package:path/path.dart' as p;
import 'package:test/test.dart';

void main() {
  final mockNowDate = DateTime.now();

  setUp(() {
    final tempDB =
        File(p.join(Directory.systemTemp.createTempSync().path, 'lento.db'));
    db.init(path: tempDB.path);
  });

  tearDown(db.reset);

  test('return empty list when conversion to queue performed on empty map', () {
    final res = withClock(
      Clock(() => mockNowDate),
      () => NotifManager().buildBannerQueue({}),
    );
    expect([], res);
  });

  test('correctly convert banner map into queue', () {
    final banners = {
      '38e03105-7723-4df3-b635-e0cd54571a9d': {
        'title': 'test title',
        'message': 'test-msg',
        'triggerTimes': [24],
      }
    };
    final res = withClock(
      Clock(() => mockNowDate),
      () => NotifManager().buildBannerQueue(banners),
    );
    expect(res, isList);
    expect(res, hasLength(1));
    expect(res[0], TypeMatcher<BannerNotif>());
    expect(res[0].title, 'test title');
    expect(res[0].triggerTime, mockNowDate.add(Duration(seconds: 24)));
  });

  test('correctly sort banner queue', () {
    final banners = {
      '38e03105-7723-4df3-b635-e0cd54571a9d': {
        'title': 'test-title',
        'message': 'test-msg',
        'triggerTimes': [903],
      },
      '94183735-7238-4d83-a07c-5bdf952d6b1a': {
        'title': 'test2_title',
        'message': 'test2_msg',
        'triggerTimes': [1],
      }
    };
    final res = withClock(
      Clock(() => mockNowDate),
      () => NotifManager().buildBannerQueue(banners),
    );
    expect(res, hasLength(2));
    expect(res[0].triggerTime, mockNowDate.add(Duration(seconds: 1)));
    expect(res[0].title, 'test2_title');
    expect(res[1].triggerTime, mockNowDate.add(Duration(seconds: 903)));
    expect(res[1].title, 'test-title');
  });

  test('correctly convert map with multi-trigger banners to queue', () {
    final banners = {
      '6667e5cf-8cd2-499e-9414-ce6531aaf3d0': {
        'title': 'banner1 title',
        'message': 'banner1 msg',
        'triggerTimes': [20, 400],
      },
      '38e03105-7723-4df3-b635-e0cd54571a9d': {
        'title': 'banner2 title',
        'message': 'banner2 msg',
        'triggerTimes': [33, 79],
      }
    };
    final res = withClock(
      Clock(() => mockNowDate),
      () => NotifManager().buildBannerQueue(banners),
    );
    expect(res, hasLength(4));
    expect(res[0].triggerTime, mockNowDate.add(Duration(seconds: 20)));
    expect(res[1].triggerTime, mockNowDate.add(Duration(seconds: 33)));
    expect(res[2].triggerTime, mockNowDate.add(Duration(seconds: 79)));
    expect(res[3].triggerTime, mockNowDate.add(Duration(seconds: 400)));
  });

  test('return null when checking for triggered banners on empty queue', () {
    expect(
        withClock(
          Clock(() => mockNowDate),
          () => NotifManager().checkForTriggeredBanners([]),
        ),
        isNull);
    final dbRes = db.getBannerQueue();
    expect(dbRes, hasLength(0));
  });

  test('return null when no banners past triggertime', () {
    final fakeBanners = [
      BannerNotif(
          title: 'title1',
          message: 'message1',
          triggerTime: mockNowDate.add(Duration(seconds: 1))),
    ];
    db.saveBannerQueue(fakeBanners);

    final res = withClock(Clock(() => mockNowDate),
        () => NotifManager().checkForTriggeredBanners(fakeBanners));
    final dbRes = db.getBannerQueue();
    expect(res, isNull);
    expect(dbRes, hasLength(1));
  });

  test('return banner at top of queue when exactly at triggertime', () {
    final fakeBanners = [
      BannerNotif(
          title: 'title1', message: 'message1', triggerTime: mockNowDate),
      BannerNotif(
          title: 'title2',
          message: 'message2',
          triggerTime: mockNowDate.add(Duration(seconds: 3))),
    ];
    db.saveBannerQueue(fakeBanners);

    final res = withClock(Clock(() => mockNowDate),
        () => NotifManager().checkForTriggeredBanners(fakeBanners));
    final dbRes = db.getBannerQueue();
    expect(res, TypeMatcher<BannerNotif>());
    expect(res!.title, 'title1');
    expect(dbRes, hasLength(1));
  });

  test('return banner at top of queue when after triggertime', () {
    final fakeBanners = [
      BannerNotif(
          title: 'title-1',
          message: 'message-1',
          triggerTime: mockNowDate.subtract(Duration(seconds: 1))),
      BannerNotif(
          title: 'title-2',
          message: 'message-2',
          triggerTime: mockNowDate.add(Duration(seconds: 4))),
    ];
    db.saveBannerQueue(fakeBanners);

    final res = withClock(Clock(() => mockNowDate),
        () => NotifManager().checkForTriggeredBanners(fakeBanners));
    final dbRes = db.getBannerQueue();
    expect(res, TypeMatcher<BannerNotif>());
    expect(res!.title, 'title-1');
    expect(dbRes, hasLength(1));
  });
}
