class ApiConfig {
  const ApiConfig._();

  static const baseUrl = String.fromEnvironment(
    'NAVIGO_API_BASE_URL',
    defaultValue: 'https://navigo-locate-production.up.railway.app/api/v1',
  );
}
