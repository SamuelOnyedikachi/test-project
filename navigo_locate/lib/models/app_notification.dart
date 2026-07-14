class AppNotification {
  const AppNotification({
    required this.id,
    required this.title,
    required this.message,
    required this.scope,
    required this.showAsPopup,
    required this.createdAt,
    required this.isRead,
    required this.payload,
  });

  factory AppNotification.fromJson(Map<String, dynamic> json) {
    return AppNotification(
      id: json['id'] as int,
      title: json['title'] as String? ?? 'Navigo notification',
      message: json['message'] as String? ?? '',
      scope: json['scope'] as String? ?? 'system',
      showAsPopup: json['show_as_popup'] as bool? ?? false,
      createdAt:
          DateTime.tryParse(json['created_at'] as String? ?? '') ??
          DateTime.now(),
      isRead: json['read_at'] != null,
      payload: Map<String, dynamic>.from(json['payload'] as Map? ?? const {}),
    );
  }

  final int id;
  final String title;
  final String message;
  final String scope;
  final bool showAsPopup;
  final DateTime createdAt;
  final bool isRead;
  final Map<String, dynamic> payload;
}
