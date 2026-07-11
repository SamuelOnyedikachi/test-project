import 'package:dio/dio.dart';

import '../config/api_config.dart';

class ApiClient {
  ApiClient({Dio? dio})
    : _dio =
          dio ??
          Dio(
            BaseOptions(
              baseUrl: _normalizedBaseUrl,
              connectTimeout: const Duration(seconds: 30),
              receiveTimeout: const Duration(seconds: 30),
              headers: {'Content-Type': 'application/json'},
            ),
          );

  final Dio _dio;

  static String get _normalizedBaseUrl {
    final baseUrl = ApiConfig.baseUrl;
    return baseUrl.endsWith('/') ? baseUrl : '$baseUrl/';
  }

  Future<Response<dynamic>> post(
    String path, {
    required Map<String, dynamic> data,
    String? accessToken,
  }) {
    return _dio.post(
      _normalizePath(path),
      data: data,
      options: Options(
        headers: accessToken == null
            ? null
            : {'Authorization': 'Bearer $accessToken'},
      ),
    );
  }

  Future<Response<dynamic>> get(String path, {String? accessToken}) {
    return _dio.get(
      _normalizePath(path),
      options: Options(
        headers: accessToken == null
            ? null
            : {'Authorization': 'Bearer $accessToken'},
      ),
    );
  }

  String _normalizePath(String path) {
    if (path.startsWith('/')) {
      return path.substring(1);
    }
    return path;
  }
}
