class ApiConfig {
  const ApiConfig._();

  static const baseUrl = String.fromEnvironment(
    'NAVIGO_API_BASE_URL',
    defaultValue: 'http://localhost:8000/api/v1',
  );
}
