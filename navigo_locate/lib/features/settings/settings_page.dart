import 'package:flutter/material.dart';

import '../../core/constants/app_colors.dart';

class SettingsPage extends StatelessWidget {
  const SettingsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Safety Settings')),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: const [
          _SettingsTile(
            icon: Icons.lock_outline,
            title: 'Emergency authorization',
            subtitle: 'Only trusted contacts and responders can view sessions.',
          ),
          _SettingsTile(
            icon: Icons.timer_outlined,
            title: 'Session expiry',
            subtitle:
                'Live links should expire automatically after a set time.',
          ),
          _SettingsTile(
            icon: Icons.fact_check_outlined,
            title: 'Audit logs',
            subtitle: 'Record every person or app that views a location.',
          ),
          _SettingsTile(
            icon: Icons.cloud_sync_outlined,
            title: 'Offline queue',
            subtitle: 'Keep GPS points locally and sync when network returns.',
          ),
        ],
      ),
    );
  }
}

class _SettingsTile extends StatelessWidget {
  const _SettingsTile({
    required this.icon,
    required this.title,
    required this.subtitle,
  });

  final IconData icon;
  final String title;
  final String subtitle;

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: const Color(0xFFE4E7EC)),
      ),
      child: Row(
        children: [
          CircleAvatar(
            backgroundColor: AppColors.primary.withValues(alpha: .1),
            child: Icon(icon, color: AppColors.primary),
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: const TextStyle(fontWeight: FontWeight.w700),
                ),
                const SizedBox(height: 4),
                Text(subtitle, style: const TextStyle(color: AppColors.grey)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
