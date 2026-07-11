import 'dart:math' as math;

import 'location_snapshot.dart';

class DestinationRoute {
  const DestinationRoute({
    required this.label,
    required this.latitude,
    required this.longitude,
    required this.startedLatitude,
    required this.startedLongitude,
  });

  final String label;
  final double latitude;
  final double longitude;
  final double startedLatitude;
  final double startedLongitude;

  double distanceFrom(LocationSnapshot location) {
    return _distanceMeters(
      location.latitude,
      location.longitude,
      latitude,
      longitude,
    );
  }

  double totalDistanceMeters() {
    return _distanceMeters(
      startedLatitude,
      startedLongitude,
      latitude,
      longitude,
    );
  }

  double bearingFrom(LocationSnapshot location) {
    final startLat = _radians(location.latitude);
    final startLon = _radians(location.longitude);
    final endLat = _radians(latitude);
    final endLon = _radians(longitude);
    final deltaLon = endLon - startLon;

    final y = math.sin(deltaLon) * math.cos(endLat);
    final x =
        math.cos(startLat) * math.sin(endLat) -
        math.sin(startLat) * math.cos(endLat) * math.cos(deltaLon);
    return (_degrees(math.atan2(y, x)) + 360) % 360;
  }

  double progressFrom(LocationSnapshot location) {
    final total = totalDistanceMeters();
    if (total <= 0) return 1;
    final remaining = distanceFrom(location);
    return ((total - remaining) / total).clamp(0, 1);
  }

  List<String> stepsFrom(LocationSnapshot? location) {
    if (location == null) {
      return [
        'Start live tracking and wait for your current GPS point.',
        'Navigo will calculate the route to $label.',
      ];
    }

    final remaining = distanceFrom(location);
    final bearing = bearingFrom(location);
    final direction = _compassDirection(bearing);

    return [
      'Head $direction toward $label.',
      'Continue for ${_formatDistance(remaining)}.',
      remaining <= 50
          ? 'You are close to your destination.'
          : 'Keep tracking. Navigo will update this as you move.',
    ];
  }
}

String formatRouteDistance(double meters) => _formatDistance(meters);

double _distanceMeters(double lat1, double lon1, double lat2, double lon2) {
  const earthRadiusMeters = 6371000;
  final phi1 = _radians(lat1);
  final phi2 = _radians(lat2);
  final deltaPhi = _radians(lat2 - lat1);
  final deltaLambda = _radians(lon2 - lon1);

  final a =
      math.sin(deltaPhi / 2) * math.sin(deltaPhi / 2) +
      math.cos(phi1) *
          math.cos(phi2) *
          math.sin(deltaLambda / 2) *
          math.sin(deltaLambda / 2);
  return earthRadiusMeters * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a));
}

double _radians(double degrees) => degrees * math.pi / 180;

double _degrees(double radians) => radians * 180 / math.pi;

String _compassDirection(double bearing) {
  const directions = [
    'north',
    'north-east',
    'east',
    'south-east',
    'south',
    'south-west',
    'west',
    'north-west',
  ];
  final index = ((bearing + 22.5) / 45).floor() % directions.length;
  return directions[index];
}

String _formatDistance(double meters) {
  if (meters >= 1000) {
    return '${(meters / 1000).toStringAsFixed(1)} km';
  }
  return '${meters.toStringAsFixed(0)} m';
}
