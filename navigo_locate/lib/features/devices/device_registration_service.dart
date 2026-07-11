import 'package:battery_plus/battery_plus.dart';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:device_info_plus/device_info_plus.dart';
import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:flutter/foundation.dart';
import 'package:geolocator/geolocator.dart';

import '../../core/network/api_client.dart';
import '../../services/location_service.dart';

class DeviceRegistrationService {
  DeviceRegistrationService({
    ApiClient? apiClient,
    DeviceInfoPlugin? deviceInfo,
    Battery? battery,
    Connectivity? connectivity,
    FirebaseMessaging? messaging,
    LocationService? locationService,
  }) : _apiClient = apiClient ?? ApiClient(),
       _deviceInfo = deviceInfo ?? DeviceInfoPlugin(),
       _battery = battery ?? Battery(),
       _connectivity = connectivity ?? Connectivity(),
       _messaging = messaging ?? FirebaseMessaging.instance,
       _locationService = locationService ?? LocationService();

  final ApiClient _apiClient;
  final DeviceInfoPlugin _deviceInfo;
  final Battery _battery;
  final Connectivity _connectivity;
  final FirebaseMessaging _messaging;
  final LocationService _locationService;

  Future<void> registerCurrentDevice({required String accessToken}) async {
    final payload = await collectDevicePayload();
    await _apiClient.post(
      '/devices/register/',
      data: payload,
      accessToken: accessToken,
    );
  }

  Future<Map<String, dynamic>> collectDevicePayload() async {
    final device = await _deviceIdentity();
    final batteryLevel = await _tryGetBatteryLevel();
    final connectivityResults = await _tryGetConnectivity();
    final fcmToken = await _tryGetFcmToken();
    final position = await _tryGetPosition();

    return {
      'device_id': device.id.length > 255
          ? device.id.substring(0, 255)
          : device.id,
      'name': device.name,
      'platform': device.platform,
      'fcm_token': fcmToken ?? '',
      'battery_level': batteryLevel,
      'network_type': connectivityResults
          .map((result) => result.name)
          .join(','),
      'last_latitude': position?.latitude.toStringAsFixed(7),
      'last_longitude': position?.longitude.toStringAsFixed(7),
      'is_active': true,
    };
  }

  Future<_DeviceIdentity> _deviceIdentity() async {
    if (kIsWeb) {
      final info = await _deviceInfo.webBrowserInfo;
      return _DeviceIdentity(
        id: info.userAgent ?? 'web-device',
        name: info.browserName.name,
        platform: 'web',
      );
    }

    if (defaultTargetPlatform == TargetPlatform.android) {
      final info = await _deviceInfo.androidInfo;
      return _DeviceIdentity(
        id: info.id,
        name: '${info.manufacturer} ${info.model}',
        platform: 'android',
      );
    }

    if (defaultTargetPlatform == TargetPlatform.iOS) {
      final info = await _deviceInfo.iosInfo;
      return _DeviceIdentity(
        id: info.identifierForVendor ?? info.name,
        name: '${info.name} ${info.model}',
        platform: 'ios',
      );
    }

    return _DeviceIdentity(
      id: defaultTargetPlatform.name,
      name: defaultTargetPlatform.name,
      platform: defaultTargetPlatform.name,
    );
  }

  Future<String?> _tryGetFcmToken() async {
    if (kIsWeb) {
      return null;
    }

    try {
      return _messaging.getToken();
    } catch (_) {
      return null;
    }
  }

  Future<int?> _tryGetBatteryLevel() async {
    try {
      return _battery.batteryLevel;
    } catch (_) {
      return null;
    }
  }

  Future<List<ConnectivityResult>> _tryGetConnectivity() async {
    try {
      return _connectivity.checkConnectivity();
    } catch (_) {
      return const [ConnectivityResult.none];
    }
  }

  Future<Position?> _tryGetPosition() async {
    try {
      await _locationService.ensurePermission();
      return _locationService.getCurrentPosition();
    } catch (_) {
      return null;
    }
  }
}

class _DeviceIdentity {
  const _DeviceIdentity({
    required this.id,
    required this.name,
    required this.platform,
  });

  final String id;
  final String name;
  final String platform;
}
