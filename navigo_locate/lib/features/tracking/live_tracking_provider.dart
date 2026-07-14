import 'dart:async';

import 'package:flutter/foundation.dart';

import '../auth/auth_service.dart';
import '../../models/destination_route.dart';
import '../../models/location_snapshot.dart';
import '../../repositories/live_tracking_repository.dart';
import '../../services/location_service.dart';
import '../../services/location_address_service.dart';

class LiveTrackingProvider extends ChangeNotifier {
  LiveTrackingProvider({
    LocationService? locationService,
    LocationAddressService? addressService,
    LiveTrackingRepository? repository,
  }) : _locationService = locationService ?? LocationService(),
       _addressService = addressService ?? LocationAddressService(),
       _repository = repository ?? LiveTrackingRepository();

  final LocationService _locationService;
  final LocationAddressService _addressService;
  final LiveTrackingRepository _repository;

  Timer? _timer;
  LocationSnapshot? _latestLocation;
  DestinationRoute? _destinationRoute;
  String? _activeSessionId;
  String? _errorMessage;
  String? _latestAddress;
  String? _addressKey;
  bool _isTracking = false;
  bool _isBusy = false;
  bool _isEmergency = false;

  LocationSnapshot? get latestLocation => _latestLocation;
  DestinationRoute? get destinationRoute => _destinationRoute;
  String? get activeSessionId => _activeSessionId;
  String? get errorMessage => _errorMessage;
  String? get latestAddress => _latestAddress;
  bool get isTracking => _isTracking;
  bool get isBusy => _isBusy;
  bool get isEmergency => _isEmergency;

  Future<void> startTracking({
    bool emergency = false,
    String? destinationLabel,
    double? destinationLatitude,
    double? destinationLongitude,
  }) async {
    if (_isTracking || _isBusy) return;

    _setBusy(true);
    _errorMessage = null;
    _isEmergency = emergency;
    notifyListeners();

    try {
      await _locationService.ensurePermission();
      final startingPosition = await _locationService.getCurrentPosition();
      final startingSnapshot = LocationSnapshot.fromPosition(startingPosition);
      _latestLocation = startingSnapshot;
      if (destinationLabel != null &&
          destinationLatitude != null &&
          destinationLongitude != null) {
        _destinationRoute = DestinationRoute(
          label: destinationLabel,
          latitude: destinationLatitude,
          longitude: destinationLongitude,
          startedLatitude: startingSnapshot.latitude,
          startedLongitude: startingSnapshot.longitude,
        );
      } else {
        _destinationRoute = null;
      }
      notifyListeners();

      final accessToken = _accessToken;

      final sessionId = await _repository.startSession(
        accessToken: accessToken,
        emergency: emergency,
      );

      _activeSessionId = sessionId;
      _isTracking = true;
      await _captureAndPublish();
      _timer = Timer.periodic(
        const Duration(seconds: 2),
        (_) => _captureAndPublish(),
      );
    } catch (error) {
      _errorMessage = error.toString();
      _isTracking = false;
      _activeSessionId = null;
      _destinationRoute = null;
      _isEmergency = false;
    } finally {
      _setBusy(false);
    }
  }

  Future<void> stopTracking() async {
    if (!_isTracking && _activeSessionId == null) return;

    final sessionId = _activeSessionId;
    _timer?.cancel();
    _timer = null;
    _isTracking = false;
    _activeSessionId = null;
    _destinationRoute = null;
    _isEmergency = false;
    notifyListeners();

    if (sessionId != null) {
      await _repository.endSession(
        accessToken: _accessToken,
        sessionId: sessionId,
      );
    }
  }

  void clearDestination() {
    _destinationRoute = null;
    notifyListeners();
  }

  Future<void> _captureAndPublish() async {
    final sessionId = _activeSessionId;
    if (sessionId == null) return;

    try {
      final position = await _locationService.getCurrentPosition();
      final snapshot = LocationSnapshot.fromPosition(position);
      _latestLocation = snapshot;
      _errorMessage = snapshot.accuracy > 5
          ? 'GPS accuracy is ${snapshot.accuracy.toStringAsFixed(0)} m. Navigo is requesting a sub-5 m fix; accuracy improves outdoors on a GPS-enabled phone.'
          : null;
      notifyListeners();
      unawaited(_resolveAddress(snapshot));

      await _repository.publishLocation(
        accessToken: _accessToken,
        sessionId: sessionId,
        snapshot: snapshot,
      );
    } catch (error) {
      _errorMessage = error.toString();
      notifyListeners();
    }
  }

  Future<void> _resolveAddress(LocationSnapshot snapshot) async {
    final key =
        '${snapshot.latitude.toStringAsFixed(4)},${snapshot.longitude.toStringAsFixed(4)}';
    if (_addressKey == key) return;
    _addressKey = key;
    try {
      final address = await _addressService.reverseGeocode(
        snapshot.latitude,
        snapshot.longitude,
      );
      if (_addressKey == key) {
        _latestAddress = address;
        notifyListeners();
      }
    } catch (_) {
      // Coordinates remain available while address lookup retries after movement.
    }
  }

  String get _accessToken {
    final token = AuthService.currentSession?.accessToken;
    if (token == null || token.isEmpty) {
      throw StateError('Please login again before starting live tracking.');
    }
    return token;
  }

  void _setBusy(bool value) {
    _isBusy = value;
    notifyListeners();
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }
}
