import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../../core/constants/app_colors.dart';
import '../../models/app_notification.dart';
import '../../services/notification_service.dart';

class NotificationsPage extends StatefulWidget {
  const NotificationsPage({super.key});

  @override
  State<NotificationsPage> createState() => _NotificationsPageState();
}

class _NotificationsPageState extends State<NotificationsPage> {
  final NotificationService _service = NotificationService();
  late Future<List<AppNotification>> _notifications;

  @override
  void initState() {
    super.initState();
    _notifications = _service.list();
  }

  void _reload() => setState(() => _notifications = _service.list());

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Notifications')),
      body: FutureBuilder<List<AppNotification>>(
        future: _notifications,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return _MessageState(
              icon: Icons.cloud_off_outlined,
              message: 'Notifications could not be loaded.',
              action: _reload,
            );
          }
          final notifications = snapshot.data ?? const [];
          if (notifications.isEmpty) {
            return const _MessageState(
              icon: Icons.notifications_none,
              message: 'No notifications yet.',
            );
          }
          return RefreshIndicator(
            onRefresh: () async => _reload(),
            child: ListView.separated(
              padding: const EdgeInsets.all(20),
              itemCount: notifications.length,
              separatorBuilder: (_, _) => const SizedBox(height: 10),
              itemBuilder: (context, index) => _NotificationItem(
                notification: notifications[index],
                onRead: () async {
                  await _service.markRead(notifications[index].id);
                  _reload();
                },
              ),
            ),
          );
        },
      ),
    );
  }
}

class _NotificationItem extends StatelessWidget {
  const _NotificationItem({required this.notification, required this.onRead});

  final AppNotification notification;
  final VoidCallback onRead;

  @override
  Widget build(BuildContext context) {
    final urgent = notification.scope == 'emergency';
    final color = urgent ? AppColors.danger : AppColors.primary;
    return Material(
      color: notification.isRead ? Colors.white : color.withValues(alpha: .06),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8),
        side: const BorderSide(color: Color(0xFFE4E7EC)),
      ),
      child: ListTile(
        onTap: notification.isRead ? null : onRead,
        contentPadding: const EdgeInsets.all(14),
        leading: CircleAvatar(
          backgroundColor: color.withValues(alpha: .1),
          child: Icon(
            urgent ? Icons.sos_rounded : Icons.notifications_outlined,
            color: color,
          ),
        ),
        title: Text(
          notification.title,
          style: const TextStyle(fontWeight: FontWeight.w800),
        ),
        subtitle: Padding(
          padding: const EdgeInsets.only(top: 6),
          child: Text(
            '${notification.message}\n${DateFormat.yMMMd().add_jm().format(notification.createdAt.toLocal())}',
          ),
        ),
        trailing: notification.isRead
            ? null
            : const Icon(Icons.circle, size: 9, color: AppColors.primary),
      ),
    );
  }
}

class _MessageState extends StatelessWidget {
  const _MessageState({required this.icon, required this.message, this.action});

  final IconData icon;
  final String message;
  final VoidCallback? action;

  @override
  Widget build(BuildContext context) => Center(
    child: Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(icon, size: 44, color: AppColors.grey),
        const SizedBox(height: 12),
        Text(message),
        if (action != null)
          TextButton(onPressed: action, child: const Text('Retry')),
      ],
    ),
  );
}
