import 'dart:io';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import 'package:path/path.dart' as p;
import 'package:pret_a_porter/pret_a_porter.dart';

import '../config.dart';

class AppSelectionForm extends StatelessWidget {
  const AppSelectionForm({
    super.key,
    required this.selectedApp,
    required this.blockItemTypeSelection,
    required this.selectedAppSetter,
  });

  final File? selectedApp;
  final BlockItemType blockItemTypeSelection;
  final Function(File?) selectedAppSetter;

  Future<File?> showAppPicker() async {
    if (Platform.isMacOS) {
      var result = await FilePicker.platform.pickFiles(
        type: FileType.custom,
        initialDirectory: '/Applications/',
        allowedExtensions: ['app'],
      );
      return result != null ? File(result.files.single.path!) : null;
    } else {
      throw 'Platform not yet supported by AppPicker!';
    }
  }

  @override
  Widget build(BuildContext context) {
    return FormField(
        validator: (_) =>
            (selectedApp == null && blockItemTypeSelection == BlockItemType.app)
                ? 'Please choose an app to block!'
                : null,
        builder: (_) => Column(children: [
              Container(
                decoration:
                    const BoxDecoration(boxShadow: [PretConfig.defaultShadow]),
                child: TextButton(
                  onPressed: () async {
                    var selection = await showAppPicker();
                    selectedAppSetter(selection);
                  },
                  style: ButtonStyle(
                    backgroundColor: MaterialStatePropertyAll(
                        Theme.of(context).colorScheme.tertiary),
                    padding: const MaterialStatePropertyAll(
                        EdgeInsets.all(PretConfig.defaultElementSpacing)),
                    shape: const MaterialStatePropertyAll(
                      RoundedRectangleBorder(
                          borderRadius: PretConfig.thinBorderRadius),
                    ),
                  ),
                  child: const Text('Choose app...'),
                ),
              ),
              const Padding(
                  padding: EdgeInsets.all(PretConfig.minElementSpacing)),
              Text(
                selectedApp != null
                    ? p.basename(selectedApp!.path)
                    : 'No app selected',
                style: Theme.of(context)
                    .textTheme
                    .labelMedium!
                    .copyWith(color: Theme.of(context).colorScheme.tertiary),
              )
            ]));
  }
}
