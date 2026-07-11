import '../../core/network/api_client.dart';

class AuthSession {
  const AuthSession({required this.accessToken, required this.refreshToken});

  final String accessToken;
  final String refreshToken;
}

class AuthService {
  AuthService({ApiClient? apiClient}) : _apiClient = apiClient ?? ApiClient();

  static AuthSession? currentSession;

  final ApiClient _apiClient;

  Future<AuthSession> login({
    required String username,
    required String password,
  }) async {
    final response = await _apiClient.post(
      '/auth/login/',
      data: {'username': username, 'password': password},
    );

    final data = response.data as Map<String, dynamic>;
    final session = AuthSession(
      accessToken: data['access'] as String,
      refreshToken: data['refresh'] as String,
    );
    currentSession = session;
    return session;
  }

  Future<void> register({
    required String username,
    required String email,
    required String fullName,
    required String phone,
    required String password,
  }) async {
    await _apiClient.post(
      '/auth/register/',
      data: {
        'username': username,
        'email': email,
        'full_name': fullName,
        'phone': phone,
        'password': password,
      },
    );
  }
}
