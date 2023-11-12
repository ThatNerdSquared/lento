import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:path_provider/path_provider.dart';
import 'package:pret_a_porter/pret_a_porter.dart';
import 'package:uuid/uuid.dart';
import 'package:window_size/window_size.dart';

import 'backend/card_data.dart';
import 'backend/icon_manager.dart';
import 'backend/popup_msg_data.dart';
import 'config.dart';
import 'widgets/blocked_item_editor.dart';
import 'widgets/card.dart';
import 'widgets/lento_toolbar.dart';

const uuID = Uuid();
final iconManager = getIconManager();
String platformAppSupportDir = '';

final lentoDeckProvider =
    StateNotifierProvider<LentoDeck, Map<String, LentoCardData>>(
        (ref) => LentoDeck());
final popupMsgsProvider =
    StateNotifierProvider<PopupMsgs, Map<String, String>>((ref) => PopupMsgs());

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
        textSelectionTheme: TextSelectionThemeData(
            selectionColor: lentoLightColorScheme.tertiary),
        shadowColor: lentoLightColorScheme.shadow,
        splashFactory: NoSplash.splashFactory,
        highlightColor: Colors.transparent,
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

  Future<void> scrollLeft() async {
    await controller.previousPage(
      duration: const Duration(seconds: 1),
      curve: Curves.decelerate,
    );
  }

  void scrollRight() => controller.nextPage(
        duration: const Duration(seconds: 1),
        curve: Curves.decelerate,
      );

  void scrollBackToStart() => controller.animateTo(
        0,
        duration: const Duration(milliseconds: 200),
        curve: Curves.decelerate,
      );

  void _onScroll() {
    final len = ref.read(lentoDeckProvider).entries.length;
    if (controller.page! > len - 0.5) {
      scrollBackToStart();
    }
  }

  @override
  Widget build(BuildContext context) {
    controller.addListener(_onScroll);
    final limitIndex = ref.watch(lentoDeckProvider).entries.length;
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
                        // why does this work?
                        if ((index - 1) == pageViewIndex) {
                          return StyledCard(child: Container());
                        }
                        final cardId = ref
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
                nextPageHandler: scrollRight,
                prevPageHandler: scrollLeft,
              )),
        ],
      ),
    )));
  }
}
