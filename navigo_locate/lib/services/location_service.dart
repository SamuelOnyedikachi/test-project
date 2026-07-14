import 'package:geolocator/geolocator.dart';

class LocationPermissionException implements Exception {
  const LocationPermissionException(this.message);

  final String message;

  @override
  String toString() => message;
}

class LocationAccuracyException implements Exception {
  const LocationAccuracyException(this.message);

  final String message;

  @override
  String toString() => message;
}

class LocationService {
  Future<void> ensurePermission() async {
    final serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      throw const LocationPermissionException(
        'Location services are disabled. Please turn on GPS to start tracking.',
      );
    }

    var permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
    }

    if (permission == LocationPermission.denied) {
      throw const LocationPermissionException(
        'Location permission is required before live tracking can start.',
      );
    }

    if (permission == LocationPermission.deniedForever) {
      throw const LocationPermissionException(
        'Location permission is permanently denied. Enable it in settings.',
      );
    }
  }

  Future<Position> getCurrentPosition() async {
    final position = await Geolocator.getCurrentPosition(
      locationSettings: const LocationSettings(
        accuracy: LocationAccuracy.bestForNavigation,
        timeLimit: Duration(seconds: 12),
      ),
    );
    if (position.accuracy > 100) {
      throw LocationAccuracyException(
        'The device returned an approximate location '
        '(${position.accuracy.toStringAsFixed(0)} m accuracy). Enable precise '
        'location, move near a window or outdoors, and wait for a GPS fix.',
      );
    }
    return position;
  }
}
