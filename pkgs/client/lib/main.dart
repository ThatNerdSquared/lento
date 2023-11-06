import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:path_provider/path_provider.dart';
import 'package:pret_a_porter/pret_a_porter.dart';
import 'package:uuid/uuid.dart';
import 'package:window_size/window_size.dart';

import 'backend/card_data.dart';
import 'backend/custom_popup_data.dart';
import 'backend/icon_manager.dart';
import 'config.dart';
import 'widgets/blocked_item_editor.dart';
import 'widgets/card.dart';
import 'widgets/lento_toolbar.dart';

const uuID = Uuid();
final iconManager = getIconManager();
String platformAppSupportDir = '';

final mockIds = [uuID.v4(), uuID.v4(), uuID.v4(), uuID.v4(), uuID.v4()];
final mockPopups = {
  mockIds[3]: const CustomPopup(
    customMessage:
        'An essential aspect of creativity is not being afraid to fail.',
  ),
  mockIds[4]: const CustomPopup(
    customMessage: 'Don\'t get distracted!',
  )
};
final lentoDeckProvider =
    StateNotifierProvider<LentoDeck, Map<String, LentoCardData>>(
        (ref) => LentoDeck());
final customPopupListProvider =
    StateNotifierProvider<CustomPopupList, Map<String, CustomPopup>>(
        (ref) => CustomPopupList(initialPopupList: mockPopups));

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  if (Platform.isWindows || Platform.isLinux || Platform.isMacOS) {
    const minHeight = 560.0;
    const minWidth = 490.0;
    setWindowMinSize(const Size(minWidth, minHeight));
    setWindowMaxSize(Size.infinite);
  }

  platformAppSupportDir = (await getApplicationDocumentsDirectory()).path;
  runApp(const ProviderScope(child: MyApp()));
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Lento',
      theme: ThemeData(
        cardTheme: lentoCardTheme,
        colorScheme: lentoLightColorScheme,
        fontFamily: 'Montserrat',
        scaffoldBackgroundColor: lentoLightColorScheme.background,
        shadowColor: lentoLightColorScheme.shadow,
        splashFactory: NoSplash.splashFactory,
        textTheme: lentoTextTheme,
      ),
      home: const LentoHome(title: 'Lento Home'),
    );
  }
}

class LentoHome extends ConsumerStatefulWidget {
  const LentoHome({super.key, required this.title});

  final String title;

  @override
  LentoHomeState createState() => LentoHomeState();
}

class LentoHomeState extends ConsumerState<LentoHome> {
  int pageViewIndex = 0;

  final PageController controller = PageController(
    viewportFraction: 0.8,
  );
  EditingEnv? editingEnv;

  @override
  Widget build(BuildContext context) {
    final limitIndex = ref.read(lentoDeckProvider).entries.length;
    return Scaffold(
        body: Center(
            child: Padding(
      padding: const EdgeInsets.only(top: PretConfig.titleBarSafeArea),
      child: Column(
        children: [
          Flexible(
              flex: 5,
              child: Container(
                  constraints: const BoxConstraints(
                    maxWidth: 700.0,
                    maxHeight: 800.0,
                  ),
                  child: PageView.builder(
                      controller: controller,
                      onPageChanged: (value) => setState(() {
                            pageViewIndex = value % limitIndex;
                          }),
                      itemBuilder: (context, index) {
                        var cardId = ref
                            .read(lentoDeckProvider)
                            .keys
                            .elementAt(index % limitIndex);
                        return editingEnv != null
                            ? BlockedItemEditor(
                                editingEnv: editingEnv!,
                                endEditing: () => setState(() {
                                  editingEnv = null;
                                }),
                              )
                            : LentoCard(
                                cardId: cardId,
                                startEditing: ({blockItemId, blockItemType}) =>
                                    setState(() {
                                      editingEnv = EditingEnv(
                                        cardId: cardId,
                                        blockItemId: blockItemId,
                                        blockItemType: blockItemType,
                                      );
                                    }));
                      }))),
          Flexible(
              flex: 1,
              child: LentoToolbar(
                currentCardIndex: pageViewIndex,
              )),
        ],
      ),
    )));
  }
}
