import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:pret_a_porter/pret_a_porter.dart';

import '../main.dart';

Menu popupMsgContextMenu(WidgetRef ref, String popupId) => Menu(
      items: [
        MenuItem(
            label: 'Delete Popup Message',
            onClick: (_) => ref
                .read(popupMsgsProvider.notifier)
                .removePopup(popupId: popupId))
      ],
    );

class NewPopupMsgForm extends ConsumerStatefulWidget {
  const NewPopupMsgForm({super.key});

  @override
  NewPopupMsgFormState createState() => NewPopupMsgFormState();
}

class NewPopupMsgFormState extends ConsumerState<NewPopupMsgForm> {
  final _formKey = GlobalKey<FormState>();
  final _textFieldController = TextEditingController();

  void onSubmit() {
    if (!_formKey.currentState!.validate()) return;
    ref
        .read(popupMsgsProvider.notifier)
        .addPopup(_textFieldController.value.text);
    _textFieldController.clear();
  }

  @override
  Widget build(BuildContext context) {
    const defaultFormFieldBorder = OutlineInputBorder(
      borderSide: BorderSide(width: 0.8),
      borderRadius: PretConfig.thinBorderRadius,
    );
    return Form(
      key: _formKey,
      child: Padding(
        padding: const EdgeInsets.only(
          left: PretConfig.thinElementSpacing,
          right: PretConfig.thinElementSpacing,
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Expanded(
              child: TextFormField(
                controller: _textFieldController,
                cursorColor: Colors.grey,
                decoration: InputDecoration(
                  border: defaultFormFieldBorder,
                  enabledBorder: defaultFormFieldBorder,
                  errorBorder: defaultFormFieldBorder,
                  focusedErrorBorder: defaultFormFieldBorder,
                  focusedBorder: defaultFormFieldBorder,
                  filled: true,
                  fillColor: Theme.of(context).colorScheme.surface,
                  focusColor: Theme.of(context).colorScheme.surface,
                  contentPadding: const EdgeInsets.all(
                    PretConfig.thinElementSpacing,
                  ),
                  hintText: 'Don\'t get distracted!',
                  isDense: true,
                ),
                validator: (value) =>
                    value!.isEmpty ? 'Please enter a popup message!' : null,
              ),
            ),
            const Padding(
                padding: EdgeInsets.only(left: PretConfig.thinElementSpacing)),
            SizedBox(
              width: 32,
              height: 32,
              child: ClipRRect(
                borderRadius: PretConfig.thinBorderRadius,
                child: Material(
                  child: Ink(
                    decoration: ShapeDecoration(
                      color: Theme.of(context).colorScheme.tertiary,
                      shape: const RoundedRectangleBorder(
                          borderRadius: PretConfig.thinBorderRadius),
                    ),
                    child: IconButton(
                      padding: EdgeInsets.zero,
                      icon: const Icon(Icons.add),
                      color: Colors.white,
                      onPressed: onSubmit,
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
