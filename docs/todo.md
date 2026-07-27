streets name not showing on map, no landmarks, on the web and django admin, use logo for the site icon

landmark, fueling station, hospital, halls etc are not visible on the map

the map on the app is not showing. also on the admin geofencing area let there be map and we'll be able to select or highlight geofenced area using a rectangular or sqare shape and also get the distance in km and also it should automatically show the longitude and latitude and also accurate radius meter.
on select users there should be option to send to all users that are registered and on the app(message should be a pop-up notification), give discreptions of the required payloads, scope etc when filling the form data based on the required data.and lastly the location address should always show the name of the location, buildings, streets, LGA for mapping and routing. also accuracy should be less than 5meters, movements done by users on the admin map should have features like distance per step, time stamp at each steps, time taken from one point to another just like google map feature.


also i noticed the app only greets Good morning with my name "samuel".
it should greet based on diffrernt location time zone and time stamp along side with users Username


For this project, run these from navigo_locate/:
# Android release APK
flutter pub get
flutter build apk --release \
  --dart-define=NAVIGO_API_BASE_URL=https://navigo-locate-production.up.railway.app/api/v1 \
  --dart-define=GOOGLE_MAPS_ANDROID_API_KEY=YOUR_ANDROID_MAPS_KEY
The APK will be at build/app/outputs/flutter-apk/app-release.apk.
For iOS, you must build on macOS with Xcode installed:
flutter pub get
cd ios
pod install
cd ..
flutter build ipa --release \
  --dart-define=NAVIGO_API_BASE_URL=https://navigo-locate-production.up.railway.app/api/v1
The IPA/archive output will be under build/ios/ipa/. Before distribution, open ios/Runner.xcworkspace in Xcode and configure your Apple Developer Team, bundle identifier, signing certificate, provisioning profile, and the iOS Google Maps API key. The Android build currently running here is still active; I’ll finish validating its artifact and include the exact path and checksum.




Small correction to the Android command above: this project’s Gradle file reads the Maps key from an environment variable, not a Dart define. Use GOOGLE_MAPS_ANDROID_API_KEY=YOUR_KEY flutter build apk ...; I’ll include the corrected complete command in the final handoff.


flutter pub get
cd ios
pod install
cd ..
flutter build ipa --release \
  --dart-define=NAVIGO_API_BASE_URL=https://navigo-locate-production.up.railway.app/api/v1

  # Android release APK
flutter pub get
flutter build apk --release \
  --dart-define=NAVIGO_API_BASE_URL=https://navigo-locate-production.up.railway.app/api/v1 \
  --dart-define=GOOGLE_MAPS_ANDROID_API_KEY=YOUR_ANDROID_MAPS_KEY




  For this project, run these from navigo_locate/:
# Android release APK
flutter pub get
flutter build apk --release \
  --dart-define=NAVIGO_API_BASE_URL=https://navigo-locate-production.up.railway.app/api/v1 \
  --dart-define=GOOGLE_MAPS_ANDROID_API_KEY=YOUR_ANDROID_MAPS_KEY
The APK will be at build/app/outputs/flutter-apk/app-release.apk.
For iOS, you must build on macOS with Xcode installed:
flutter pub get
cd ios
pod install
cd ..
flutter build ipa --release \
  --dart-define=NAVIGO_API_BASE_URL=https://navigo-locate-production.up.railway.app/api/v1
The IPA/archive output will be under build/ios/ipa/. Before distribution, open ios/Runner.xcworkspace in Xcode and configure your Apple Developer Team, bundle identifier, signing certificate, provisioning profile, and the iOS Google Maps API key. The Android build currently running here is still active; I’ll finish validating its artifact and include the exact path and checksum.




Small correction to the Android command above: this project’s Gradle file reads the Maps key from an environment variable, not a Dart define. Use GOOGLE_MAPS_ANDROID_API_KEY=YOUR_KEY flutter build apk ...; I’ll include the corrected complete command in the final handoff.







The restarted APK build has passed the earlier JNI failure and completed Dart/icon optimization; it’s now in final native packaging. The only emitted message is a future Flutter compatibility warning from firebase_database, not a build failure.



















Approve for me







5.6 SolLight










Work locallyLocal