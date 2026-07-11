import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../app/router.dart';
import '../../core/constants/app_assets.dart';
import '../../core/constants/app_colors.dart';
import '../../shared/widgets/info_card.dart';
import '../contacts/contacts_provider.dart';
import '../tracking/live_tracking_provider.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer2<LiveTrackingProvider, ContactsProvider>(
      builder: (context, tracking, contacts, _) {
        final location = tracking.latestLocation;
        final isActive = tracking.isTracking || tracking.isBusy;

        return Scaffold(
          backgroundColor: AppColors.lightGrey,
          appBar: AppBar(
            title: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                ClipRRect(
                  borderRadius: BorderRadius.circular(5),
                  child: Image.asset(
                    AppAssets.logo,
                    width: 42,
                    height: 30,
                    fit: BoxFit.cover,
                    filterQuality: FilterQuality.medium,
                  ),
                ),
                const SizedBox(width: 10),
                const Text('NaviGo-Locate'),
              ],
            ),
            actions: [
              IconButton(
                onPressed: () =>
                    Navigator.pushNamed(context, Routes.notifications),
                icon: const Icon(Icons.notifications_none),
              ),
            ],
          ),
          body: SingleChildScrollView(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Good Morning,',
                  style: TextStyle(color: AppColors.grey),
                ),
                const SizedBox(height: 4),
                const Text(
                  'Samuel',
                  style: TextStyle(fontSize: 30, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 20),

                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    color: tracking.isEmergency
                        ? AppColors.danger
                        : AppColors.primary,
                    borderRadius: BorderRadius.circular(24),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        tracking.isTracking
                            ? tracking.isEmergency
                                  ? 'SOS Mode Active'
                                  : 'Live Tracking Active'
                            : 'You are Safe',
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        tracking.isTracking
                            ? 'Your location is updating every 2 seconds.'
                            : 'Live tracking is currently off.',
                        style: const TextStyle(color: Colors.white70),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 20),

                InfoCard(
                  icon: Icons.location_on_outlined,
                  title: 'Current Coordinates',
                  value: location == null
                      ? 'Waiting for GPS'
                      : '${location.latitude.toStringAsFixed(5)}, ${location.longitude.toStringAsFixed(5)}',
                  color: AppColors.primary,
                ),
                const SizedBox(height: 14),

                InfoCard(
                  icon: Icons.gps_fixed,
                  title: 'GPS Accuracy',
                  value: location == null
                      ? '-- meters'
                      : '${location.accuracy.toStringAsFixed(0)} meters',
                  color: Colors.green,
                ),
                const SizedBox(height: 14),

                InfoCard(
                  icon: Icons.speed_rounded,
                  title: 'Speed',
                  value: location == null
                      ? '-- m/s'
                      : '${location.speed.toStringAsFixed(1)} m/s',
                  color: Colors.orange,
                ),
                const SizedBox(height: 14),

                InfoCard(
                  icon: Icons.wifi,
                  title: 'Tracking Status',
                  value: tracking.isTracking ? 'Online' : 'Inactive',
                  color: Colors.purple,
                ),

                if (tracking.destinationRoute != null) ...[
                  const SizedBox(height: 14),
                  InfoCard(
                    icon: Icons.route_outlined,
                    title: 'Destination',
                    value: tracking.destinationRoute!.label,
                    color: AppColors.primary,
                  ),
                ],

                if (tracking.errorMessage != null) ...[
                  const SizedBox(height: 16),
                  Text(
                    tracking.errorMessage!,
                    style: const TextStyle(color: AppColors.danger),
                  ),
                ],

                const SizedBox(height: 24),

                GridView.count(
                  crossAxisCount: MediaQuery.of(context).size.width > 640
                      ? 4
                      : 2,
                  shrinkWrap: true,
                  physics: const NeverScrollableScrollPhysics(),
                  mainAxisSpacing: 12,
                  crossAxisSpacing: 12,
                  childAspectRatio: 1.65,
                  children: [
                    _HomeActionTile(
                      icon: Icons.map_outlined,
                      title: 'Live Map',
                      subtitle: tracking.isTracking
                          ? 'Open session'
                          : 'No active session',
                      onTap: tracking.isTracking
                          ? () => Navigator.pushNamed(context, Routes.liveMap)
                          : null,
                    ),
                    _HomeActionTile(
                      icon: Icons.people_alt_outlined,
                      title: 'Contacts',
                      subtitle: '${contacts.contacts.length} trusted',
                      onTap: () =>
                          Navigator.pushNamed(context, Routes.contacts),
                    ),
                    _HomeActionTile(
                      icon: Icons.timeline_outlined,
                      title: 'History',
                      subtitle: 'Route timeline',
                      onTap: () => Navigator.pushNamed(context, Routes.history),
                    ),
                    _HomeActionTile(
                      icon: Icons.settings_outlined,
                      title: 'Settings',
                      subtitle: 'Safety controls',
                      onTap: () =>
                          Navigator.pushNamed(context, Routes.settings),
                    ),
                  ],
                ),

                const SizedBox(height: 24),

                SizedBox(
                  width: double.infinity,
                  height: 54,
                  child: ElevatedButton.icon(
                    onPressed: isActive
                        ? null
                        : () => _startTracking(context, emergency: false),
                    icon: tracking.isBusy
                        ? const SizedBox(
                            width: 18,
                            height: 18,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          )
                        : const Icon(Icons.play_arrow_rounded),
                    label: const Text('Start Live Tracking'),
                  ),
                ),

                const SizedBox(height: 16),

                SizedBox(
                  width: double.infinity,
                  height: 54,
                  child: OutlinedButton.icon(
                    onPressed: isActive
                        ? null
                        : () => _showDestinationSheet(context),
                    icon: const Icon(Icons.route_outlined),
                    label: const Text('Route to Destination'),
                  ),
                ),

                const SizedBox(height: 16),

                SizedBox(
                  width: double.infinity,
                  height: 54,
                  child: ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.danger,
                      foregroundColor: Colors.white,
                    ),
                    onPressed: isActive
                        ? null
                        : () => _startTracking(context, emergency: true),
                    icon: const Icon(Icons.sos),
                    label: const Text('SOS Emergency'),
                  ),
                ),

                if (tracking.isTracking) ...[
                  const SizedBox(height: 16),
                  SizedBox(
                    width: double.infinity,
                    height: 54,
                    child: OutlinedButton.icon(
                      onPressed: () {
                        Navigator.pushNamed(context, Routes.liveMap);
                      },
                      icon: const Icon(Icons.map_outlined),
                      label: const Text('Open Live Map'),
                    ),
                  ),
                  const SizedBox(height: 16),
                  SizedBox(
                    width: double.infinity,
                    height: 54,
                    child: OutlinedButton.icon(
                      onPressed: () =>
                          _shareLiveMap(context, tracking, contacts),
                      icon: const Icon(Icons.ios_share_outlined),
                      label: const Text('Share Live Map'),
                    ),
                  ),
                ],
              ],
            ),
          ),
        );
      },
    );
  }

  Future<void> _startTracking(
    BuildContext context, {
    required bool emergency,
    String? destinationLabel,
    double? destinationLatitude,
    double? destinationLongitude,
  }) async {
    final tracking = context.read<LiveTrackingProvider>();
    await tracking.startTracking(
      emergency: emergency,
      destinationLabel: destinationLabel,
      destinationLatitude: destinationLatitude,
      destinationLongitude: destinationLongitude,
    );

    if (!context.mounted) return;
    if (tracking.isTracking) {
      Navigator.pushNamed(context, Routes.liveMap);
    } else if (tracking.errorMessage != null) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text(tracking.errorMessage!)));
    }
  }

  void _showDestinationSheet(BuildContext context) {
    final labelController = TextEditingController();
    final latitudeController = TextEditingController();
    final longitudeController = TextEditingController();

    showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      builder: (sheetContext) {
        return Padding(
          padding: EdgeInsets.only(
            left: 20,
            right: 20,
            top: 20,
            bottom: MediaQuery.of(sheetContext).viewInsets.bottom + 20,
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Where are you going?',
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.w700),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: labelController,
                decoration: const InputDecoration(
                  labelText: 'Destination name',
                  prefixIcon: Icon(Icons.place_outlined),
                ),
              ),
              const SizedBox(height: 12),
              TextField(
                controller: latitudeController,
                keyboardType: const TextInputType.numberWithOptions(
                  signed: true,
                  decimal: true,
                ),
                decoration: const InputDecoration(
                  labelText: 'Destination latitude',
                  prefixIcon: Icon(Icons.explore_outlined),
                ),
              ),
              const SizedBox(height: 12),
              TextField(
                controller: longitudeController,
                keyboardType: const TextInputType.numberWithOptions(
                  signed: true,
                  decimal: true,
                ),
                decoration: const InputDecoration(
                  labelText: 'Destination longitude',
                  prefixIcon: Icon(Icons.explore_outlined),
                ),
              ),
              const SizedBox(height: 18),
              SizedBox(
                width: double.infinity,
                height: 52,
                child: ElevatedButton.icon(
                  onPressed: () {
                    final label = labelController.text.trim();
                    final latitude = double.tryParse(
                      latitudeController.text.trim(),
                    );
                    final longitude = double.tryParse(
                      longitudeController.text.trim(),
                    );

                    if (label.isEmpty ||
                        latitude == null ||
                        longitude == null) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text(
                            'Enter a name, latitude, and longitude.',
                          ),
                        ),
                      );
                      return;
                    }

                    Navigator.pop(sheetContext);
                    _startTracking(
                      context,
                      emergency: false,
                      destinationLabel: label,
                      destinationLatitude: latitude,
                      destinationLongitude: longitude,
                    );
                  },
                  icon: const Icon(Icons.navigation_outlined),
                  label: const Text('Start Route'),
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  void _shareLiveMap(
    BuildContext context,
    LiveTrackingProvider tracking,
    ContactsProvider contacts,
  ) {
    final viewers = contacts.contacts
        .where((contact) => contact.permissions.canViewLiveLocation)
        .length;
    final session = tracking.activeSessionId ?? 'current';
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Live session $session shared with $viewers contacts.'),
      ),
    );
  }
}

class _HomeActionTile extends StatelessWidget {
  const _HomeActionTile({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.onTap,
  });

  final IconData icon;
  final String title;
  final String subtitle;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    final enabled = onTap != null;

    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(18),
      child: Ink(
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(18),
          border: Border.all(color: const Color(0xFFE4E7EC)),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Icon(icon, color: enabled ? AppColors.primary : AppColors.grey),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: TextStyle(
                    fontWeight: FontWeight.w700,
                    color: enabled ? AppColors.dark : AppColors.grey,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  subtitle,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(color: AppColors.grey, fontSize: 12),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
