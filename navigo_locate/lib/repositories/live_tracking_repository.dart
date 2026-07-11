import 'package:battery_plus/battery_plus.dart';
import 'package:connectivity_plus/connectivity_plus.dart';

import '../core/network/api_client.dart';
import '../models/location_snapshot.dart';

class LiveTrackingRepository {
  LiveTrackingRepository({
    ApiClient? apiClient,
    Battery? battery,
    Connectivity? connectivity,
  }) : _apiClient = apiClient ?? ApiClient(),
       _battery = battery ?? Battery(),
       _connectivity = connectivity ?? Connectivity();

  final ApiClient _apiClient;
  final Battery _battery;
  final Connectivity _connectivity;

  Future<String> startSession({
    required String accessToken,
    bool emergency = false,
  }) async {
    final response = await _apiClient.post(
      '/tracking/start/',
      accessToken: accessToken,
      data: {'emergency': emergency},
    );
    final data = response.data as Map<String, dynamic>;
    return data['id'].toString();
  }

  Future<void> publishLocation({
    required String accessToken,
    required String sessionId,
    required LocationSnapshot snapshot,
  }) async {
    await _apiClient.post(
      '/tracking/update-location/',
      accessToken: accessToken,
      data: {
        'session_id': sessionId,
        'latitude': snapshot.latitude,
        'longitude': snapshot.longitude,
        'accuracy': snapshot.accuracy,
        'altitude': snapshot.altitude,
        'heading': snapshot.heading,
        'speed': snapshot.speed,
        'battery_level': await _safeBatteryLevel(),
        'network_type': await _safeNetworkType(),
        'recorded_at': snapshot.timestamp.toUtc().toIso8601String(),
      },
    );
  }

  Future<void> endSession({
    required String accessToken,
    required String sessionId,
  }) async {
    await _apiClient.post(
      '/tracking/stop/',
      accessToken: accessToken,
      data: {'session_id': sessionId},
    );
  }

  Future<int?> _safeBatteryLevel() async {
    try {
      return await _battery.batteryLevel;
    } catch (_) {
      return null;
    }
  }

  Future<String> _safeNetworkType() async {
    try {
      final results = await _connectivity.checkConnectivity();
      if (results.isEmpty) return 'unknown';
      return results.map((result) => result.name).join(',');
    } catch (_) {
      return 'unknown';
    }
  }
}
