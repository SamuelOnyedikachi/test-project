import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:provider/provider.dart';

import '../../core/constants/app_colors.dart';
import '../tracking/live_tracking_provider.dart';

class HistoryPage extends StatelessWidget {
  const HistoryPage({super.key});

  @override
  Widget build(BuildContext context) {
    final tracking = context.watch<LiveTrackingProvider>();
    final latest = tracking.latestLocation;

    return Scaffold(
      appBar: AppBar(title: const Text('Route History')),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          _HistoryHeader(isTracking: tracking.isTracking),
          const SizedBox(height: 16),
          if (latest == null)
            const _EmptyHistory()
          else
            _TimelinePoint(
              title: tracking.isEmergency
                  ? 'Emergency tracking point'
                  : 'Latest tracking point',
              subtitle:
                  '${latest.latitude.toStringAsFixed(5)}, ${latest.longitude.toStringAsFixed(5)}',
              time: DateFormat('hh:mm:ss a').format(latest.timestamp.toLocal()),
              color: tracking.isEmergency
                  ? AppColors.danger
                  : AppColors.primary,
            ),
          const SizedBox(height: 12),
          const _TimelinePoint(
            title: 'History storage',
            subtitle:
                'Route points are saved under tracking_sessions/{id}/route_points.',
            time: 'Ready',
            color: Colors.green,
          ),
        ],
      ),
    );
  }
}

class _HistoryHeader extends StatelessWidget {
  const _HistoryHeader({required this.isTracking});

  final bool isTracking;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: const Color(0xFFE4E7EC)),
      ),
      child: Row(
        children: [
          const Icon(Icons.timeline_outlined, color: AppColors.primary),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              isTracking
                  ? 'A route timeline is being recorded now.'
                  : 'Start tracking to record a route timeline.',
              style: const TextStyle(fontWeight: FontWeight.w600),
            ),
          ),
        ],
      ),
    );
  }
}

class _EmptyHistory extends StatelessWidget {
  const _EmptyHistory();

  @override
  Widget build(BuildContext context) {
    return const Padding(
      padding: EdgeInsets.symmetric(vertical: 28),
      child: Center(
        child: Text(
          'No movement points yet.',
          style: TextStyle(color: AppColors.grey),
        ),
      ),
    );
  }
}

class _TimelinePoint extends StatelessWidget {
  const _TimelinePoint({
    required this.title,
    required this.subtitle,
    required this.time,
    required this.color,
  });

  final String title;
  final String subtitle;
  final String time;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Column(
          children: [
            CircleAvatar(radius: 8, backgroundColor: color),
            Container(width: 2, height: 58, color: const Color(0xFFE4E7EC)),
          ],
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: const Color(0xFFE4E7EC)),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  time,
                  style: const TextStyle(color: AppColors.grey, fontSize: 12),
                ),
                const SizedBox(height: 4),
                Text(
                  title,
                  style: const TextStyle(fontWeight: FontWeight.w700),
                ),
                const SizedBox(height: 4),
                Text(subtitle, style: const TextStyle(color: AppColors.grey)),
              ],
            ),
          ),
        ),
      ],
    );
  }
}
