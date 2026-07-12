import 'dart:async';
import 'dart:js_interop';

import 'package:web/web.dart' as web;

bool googleMapsReady = false;

Future<void> loadGoogleMaps() async {
  const apiKey = String.fromEnvironment('GOOGLE_MAPS_WEB_API_KEY');
  if (apiKey.isEmpty) return;

  final existing = web.document.getElementById('google-maps-sdk');
  if (existing != null) {
    googleMapsReady = true;
    return;
  }

  final completer = Completer<void>();
  final script = web.HTMLScriptElement()
    ..id = 'google-maps-sdk'
    ..async = true
    ..defer = true
    ..src = 'https://maps.googleapis.com/maps/api/js'
        '?key=${Uri.encodeQueryComponent(apiKey)}&loading=async&v=weekly';
  script.addEventListener('load', ((web.Event _) {
    googleMapsReady = true;
    completer.complete();
  }).toJS);
  script.addEventListener('error', ((web.Event _) {
    completer.completeError(
      StateError('Google Maps could not load. Check the web API key.'),
    );
  }).toJS);
  web.document.head!.appendChild(script);
  await completer.future.timeout(const Duration(seconds: 15));
}
