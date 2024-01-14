import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:pret_a_porter/pret_a_porter.dart';

import '../config.dart';
import '../main.dart';
import '../platform_daemon_settings.dart';
import 'timer_edit_wheel.dart';

class CardTimer extends ConsumerStatefulWidget {
  final String cardId;
  final Color startingColour;

  const CardTimer({
    super.key,
    required this.cardId,
    required this.startingColour,
  });

  @override
  CardTimerState createState() => CardTimerState();
}

class CardTimerState extends ConsumerState<CardTimer> {
  bool _isEditingTimer = false;
  final _formKey = GlobalKey<FormState>();
  late Color _timerColor = widget.startingColour;
  FocusNode secondsFocusNode = FocusNode();

  double _calculateTimerMargin(maxWidth, isEditingTimer) {
    if (isEditingTimer &&
        ((maxWidth * 2 * Config.defaultMarginPercentage) < 300)) {
      return 0.05 * maxWidth;
    } else {
      return Config.defaultMarginPercentage * maxWidth;
    }
  }

  void _onTimerValChanged(String value, TimeSection timeSection) {
    if (!_formKey.currentState!.validate()) return;
    ref.read(lentoDeckProvider.notifier).updateCardTime(
          cardId: widget.cardId,
          newValue: int.parse(value),
          timeSection: timeSection,
        );
  }

  @override
  Widget build(BuildContext context) {
    final blockDuration = ref.watch(
        lentoDeckProvider.select((deck) => deck[widget.cardId]!.blockDuration));
    final isCardActivated =
        ref.watch(lentoDeckProvider)[widget.cardId]!.isActivated;

    return LayoutBuilder(
      builder: (context, constraints) {
        final fullTimerWidth = constraints.maxWidth -
            2 *
                _calculateTimerMargin(
                  constraints.maxWidth,
                  _isEditingTimer,
                );
        return Column(children: [
          MouseRegion(
            onHover: (pointer) {
              setState(() {
                isCardActivated
                    ? null
                    : _timerColor = Theme.of(context).colorScheme.surfaceTint;
              });
            },
            onExit: (pointer) {
              setState(() {
                _timerColor = Theme.of(context).colorScheme.surface;
                _isEditingTimer = false;
              });
            },
            child: GestureDetector(
              onTap: () {
                setState(() {
                  if (!isCardActivated) {
                    _isEditingTimer = true;
                    secondsFocusNode.requestFocus();
                  }
                });
              },
              child: Container(
                margin: EdgeInsets.only(
                  left: _calculateTimerMargin(
                      constraints.maxWidth, _isEditingTimer),
                  right: _calculateTimerMargin(
                      constraints.maxWidth, _isEditingTimer),
                ),
                padding: const EdgeInsets.only(
                  top: PretConfig.defaultElementSpacing * 3 / 2,
                  bottom: PretConfig.defaultElementSpacing * 3 / 2,
                ),
                decoration: BoxDecoration(
                  color: _timerColor,
                  borderRadius: PretConfig.defaultBorderRadius,
                ),
                child: Column(
                  children: [
                    SizedBox(
                      width: fullTimerWidth,
                      child: Form(
                        key: _formKey,
                        child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: !_isEditingTimer
                                ? [
                                    for (final item in [
                                      blockDuration.fmtHours,
                                      ':',
                                      blockDuration.fmtMinutes,
                                      ':',
                                      blockDuration.fmtSeconds
                                    ])
                                      Text(
                                        item,
                                        style: Theme.of(context)
                                            .textTheme
                                            .displayLarge!
                                            .copyWith(
                                                fontWeight: FontWeight.w700),
                                      )
                                  ]
                                : [
                                    for (final timeSection
                                        in TimeSection.values)
                                      Padding(
                                        padding: const EdgeInsets.only(
                                          bottom:
                                              PretConfig.defaultElementSpacing,
                                        ),
                                        child: TimerEditWheel(
                                          cardId: widget.cardId,
                                          timeSection: timeSection,
                                          handleChange: _onTimerValChanged,
                                          fullTimerWidth: fullTimerWidth,
                                          focusNode:
                                              timeSection == TimeSection.seconds
                                                  ? secondsFocusNode
                                                  : null,
                                        ),
                                      )
                                  ]),
                      ),
                    ),
                    Container(
                      margin: const EdgeInsets.only(
                        top: PretConfig.thinElementSpacing,
                      ),
                      decoration: const BoxDecoration(
                        borderRadius: PretConfig.defaultBorderRadius,
                        boxShadow: [PretConfig.defaultShadow],
                      ),
                      child: ElevatedButton(
                          onPressed: isCardActivated ? null : _startTimer,
                          style: ButtonStyle(
                            foregroundColor: MaterialStatePropertyAll(
                                Theme.of(context).colorScheme.primary),
                            backgroundColor: MaterialStatePropertyAll(
                                Theme.of(context).colorScheme.tertiary),
                            textStyle: MaterialStatePropertyAll(
                                Theme.of(context).textTheme.displaySmall),
                            padding: const MaterialStatePropertyAll(
                                EdgeInsets.all(
                                    PretConfig.defaultElementSpacing)),
                            shape: const MaterialStatePropertyAll(
                                RoundedRectangleBorder(
                                    borderRadius: PretConfig.thinBorderRadius)),
                          ),
                          child: Text(isCardActivated
                              ? 'Session Started'
                              : 'Start Block')),
                    )
                  ],
                ),
              ),
            ),
          ),
        ]);
      },
    );
  }

  void _startTimer() {
    ref.read(lentoDeckProvider.notifier).activateCard(widget.cardId);
    final daemonSettings = getPlatformDaemonSettings();
    daemonSettings
        .sendBlockDataToDaemon(ref.read(lentoDeckProvider)[widget.cardId]!);

    Timer.periodic(const Duration(seconds: 1), (timer) {
      if (mounted) {
        final blockDuration = ref.read(lentoDeckProvider
            .select((deck) => deck[widget.cardId]!.blockDuration));
        final newDuration = blockDuration.gatheredSeconds - 1;
        ref.read(lentoDeckProvider.notifier).updateCardTime(
              cardId: widget.cardId,
              newValue: newDuration,
            );

        if (newDuration == 0) {
          timer.cancel();
          ref.read(lentoDeckProvider.notifier).deactivateCard(widget.cardId);
          print('timer complete'); // ignore: avoid_print
        }
      }
    });
  }
}
