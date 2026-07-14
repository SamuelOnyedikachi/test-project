import '../core/network/api_client.dart';
import '../features/auth/auth_service.dart';

class LocationAddressService {
  LocationAddressService({ApiClient? apiClient})
    : _apiClient = apiClient ?? ApiClient();

  final ApiClient _apiClient;

  Future<String> reverseGeocode(double latitude, double longitude) async {
    final token = AuthService.currentSession?.accessToken;
    if (token == null) return _coordinates(latitude, longitude);
    final response = await _apiClient.get(
      '/maps/reverse-geocode/?latitude=$latitude&longitude=$longitude',
      accessToken: token,
    );
    final data = response.data as Map<String, dynamic>;
    final parts = <String>[
      data['building'] as String? ?? '',
      data['street'] as String? ?? '',
      data['neighborhood'] as String? ?? '',
      data['locality'] as String? ?? '',
      data['lga'] as String? ?? '',
      data['state'] as String? ?? '',
    ].where((part) => part.trim().isNotEmpty).toSet().toList();
    return parts.isEmpty
        ? data['formatted_address'] as String? ??
              _coordinates(latitude, longitude)
        : parts.join(', ');
  }

  String _coordinates(double latitude, double longitude) =>
      '${latitude.toStringAsFixed(5)}, ${longitude.toStringAsFixed(5)}';
}
