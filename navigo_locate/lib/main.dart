import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';

import 'app/app.dart';
import 'firebase_options.dart';
import 'services/google_maps_loader.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  try {
    await loadGoogleMaps();
  } catch (_) {
    // The app still starts and presents a map configuration error in context.
  }

  runApp(const NavigoLocate());
}
