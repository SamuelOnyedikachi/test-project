import 'dart:async';

import 'package:flutter/material.dart';

import '../../models/app_notification.dart';
import '../../services/notification_service.dart';

class NotificationPopupHost extends StatefulWidget {
  const NotificationPopupHost({
    required this.child,
    required this.navigatorKey,
    super.key,
  });

  final Widget child;
  final GlobalKey<NavigatorState> navigatorKey;

  @override
  State<NotificationPopupHost> createState() => _NotificationPopupHostState();
}

class _NotificationPopupHostState extends State<NotificationPopupHost> {
  final NotificationService _service = NotificationService();
  final Set<int> _handled = {};
  Timer? _timer;
  bool _checking = false;
  bool _dialogOpen = false;

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(const Duration(seconds: 15), (_) => _check());
    WidgetsBinding.instance.addPostFrameCallback((_) => _check());
  }

  Future<void> _check() async {
    if (_checking || _dialogOpen || !mounted) return;
    _checking = true;
    try {
      final messages = await _service.list(unreadOnly: true);
      for (final message in messages.reversed) {
        if (!message.showAsPopup || _handled.contains(message.id)) continue;
        _handled.add(message.id);
        await _show(message);
        break;
      }
    } catch (_) {
      // Polling retries quietly; the inbox still exposes recoverable API errors.
    } finally {
      _checking = false;
    }
  }

  Future<void> _show(AppNotification message) async {
    final navigatorContext = widget.navigatorKey.currentContext;
    if (navigatorContext == null) return;
    _dialogOpen = true;
    await showDialog<void>(
      context: navigatorContext,
      builder: (dialogContext) => AlertDialog(
        icon: Icon(_iconFor(message.scope), color: _colorFor(message.scope)),
        title: Text(message.title),
        content: Text(message.message),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(dialogContext),
            child: const Text('Got it'),
          ),
        ],
      ),
    );
    _dialogOpen = false;
    try {
      await _service.markRead(message.id);
    } catch (_) {}
  }

  IconData _iconFor(String scope) => switch (scope) {
    'emergency' => Icons.sos_rounded,
    'tracking' => Icons.location_on_outlined,
    'safety' => Icons.health_and_safety_outlined,
    'account' => Icons.person_outline,
    _ => Icons.notifications_outlined,
  };

  Color _colorFor(String scope) =>
      scope == 'emergency' ? Colors.red : Colors.blue;

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => widget.child;
}
