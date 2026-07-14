import '../../core/network/api_client.dart';

class AuthUser {
  const AuthUser({
    required this.id,
    required this.username,
    this.fullName = '',
  });

  factory AuthUser.fromJson(Map<String, dynamic> json) => AuthUser(
    id: json['id'] as int? ?? 0,
    username: json['username'] as String? ?? '',
    fullName: json['full_name'] as String? ?? '',
  );

  final int id;
  final String username;
  final String fullName;
}

class AuthSession {
  const AuthSession({
    required this.accessToken,
    required this.refreshToken,
    required this.user,
  });

  final String accessToken;
  final String refreshToken;
  final AuthUser user;
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
      user: data['user'] is Map<String, dynamic>
          ? AuthUser.fromJson(data['user'] as Map<String, dynamic>)
          : AuthUser(id: 0, username: username),
    );
    currentSession = session;
    return session;
  }

  Future<String> requestPasswordReset({required String email}) async {
    final response = await _apiClient.post(
      '/auth/password-reset/request/',
      data: {'email': email},
    );
    return (response.data as Map<String, dynamic>)['detail'] as String;
  }

  Future<String> confirmPasswordReset({
    required String email,
    required String otp,
    required String newPassword,
    required String confirmPassword,
  }) async {
    final response = await _apiClient.post(
      '/auth/password-reset/confirm/',
      data: {
        'email': email,
        'otp': otp,
        'new_password': newPassword,
        'confirm_password': confirmPassword,
      },
    );
    return (response.data as Map<String, dynamic>)['detail'] as String;
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
