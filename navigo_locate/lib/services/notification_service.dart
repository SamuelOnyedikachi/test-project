import '../core/network/api_client.dart';
import '../features/auth/auth_service.dart';
import '../models/app_notification.dart';

class NotificationService {
  NotificationService({ApiClient? apiClient})
    : _apiClient = apiClient ?? ApiClient();

  final ApiClient _apiClient;

  Future<List<AppNotification>> list({bool unreadOnly = false}) async {
    final token = AuthService.currentSession?.accessToken;
    if (token == null) return const [];
    final response = await _apiClient.get(
      unreadOnly ? '/notifications/?unread=true' : '/notifications/',
      accessToken: token,
    );
    final data = response.data as List<dynamic>;
    return data
        .map((item) => AppNotification.fromJson(item as Map<String, dynamic>))
        .toList();
  }

  Future<void> markRead(int id) async {
    final token = AuthService.currentSession?.accessToken;
    if (token == null) return;
    await _apiClient.patch('/notifications/$id/', accessToken: token);
  }
}
