import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:share_plus/share_plus.dart';

import '../../app/router.dart';
import '../../shared/widgets/fynder_widgets.dart';
import '../profile/profile_provider.dart';
import '../tracking/live_tracking_provider.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  bool _shared = false;

  Future<void> _shareLocation() async {
    final tracking = context.read<LiveTrackingProvider>();
    if (!tracking.isTracking) {
      await tracking.startTracking();
      if (!mounted) return;
      if (!tracking.isTracking) {
        final message =
            tracking.errorMessage ?? 'Unable to start location sharing.';
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text(message)));
        return;
      }
    }

    final point = tracking.latestLocation;
    final link = point == null
        ? 'Fynder live session: ${tracking.activeSessionId ?? 'active'}'
        : 'I’m sharing my live location with Fynder: '
              'https://maps.google.com/?q=${point.latitude},${point.longitude}';
    await SharePlus.instance.share(
      ShareParams(text: link, subject: 'My live location'),
    );
    if (mounted) setState(() => _shared = true);
  }

  @override
  Widget build(BuildContext context) {
    final tracking = context.watch<LiveTrackingProvider>();
    final profile = context.watch<ProfileProvider>();
    final active = tracking.isTracking;

    return Scaffold(
      body: SafeArea(
        child: LayoutBuilder(
          builder: (context, constraints) => SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 23),
            child: ConstrainedBox(
              constraints: BoxConstraints(minHeight: constraints.maxHeight),
              child: Column(
                children: [
                  const SizedBox(height: 24),
                  const FynderHeader(),
                  const SizedBox(height: 38),
                  _LocationCard(
                    profile: profile,
                    tracking: tracking,
                    onProfileTap: () =>
                        Navigator.pushNamed(context, Routes.profile),
                  ),
                  const SizedBox(height: 24),
                  SizedBox(
                    width: double.infinity,
                    height: 54,
                    child: ElevatedButton.icon(
                      onPressed: tracking.isBusy ? null : _shareLocation,
                      icon: tracking.isBusy
                          ? const SizedBox(
                              width: 18,
                              height: 18,
                              child: CircularProgressIndicator(
                                strokeWidth: 2,
                                color: Colors.white,
                              ),
                            )
                          : _shared
                          ? const SizedBox.shrink()
                          : const Icon(Icons.ios_share_outlined),
                      label: Text(
                        _shared ? 'Location shared!' : 'Share My Location',
                      ),
                    ),
                  ),
                  const SizedBox(height: 24),
                  _SharingStatus(active: active),
                  const SizedBox(height: 150),
                  const ControlFooter(),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _LocationCard extends StatelessWidget {
  const _LocationCard({
    required this.profile,
    required this.tracking,
    required this.onProfileTap,
  });

  final ProfileProvider profile;
  final LiveTrackingProvider tracking;
  final VoidCallback onProfileTap;

  @override
  Widget build(BuildContext context) {
    final address =
        tracking.latestAddress ?? 'Waiting for your current location';
    final location = tracking.latestLocation;
    final coordinate = location == null
        ? 'GPS location'
        : '${location.latitude.toStringAsFixed(4)}, ${location.longitude.toStringAsFixed(4)}';

    return Container(
      decoration: BoxDecoration(
        color: Theme.of(context).cardColor,
        borderRadius: BorderRadius.circular(16),
        boxShadow: Theme.of(context).brightness == Brightness.light
            ? const [
                BoxShadow(
                  color: Color(0x0D000000),
                  blurRadius: 18,
                  offset: Offset(0, 8),
                ),
              ]
            : null,
      ),
      child: Column(
        children: [
          InkWell(
            onTap: onProfileTap,
            borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 24),
              child: Row(
                children: [
                  ProfileAvatar(
                    index: profile.avatarIndex,
                    galleryImage: profile.galleryImage,
                    size: 56,
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          profile.name,
                          style: const TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w800,
                          ),
                        ),
                        const SizedBox(height: 3),
                        const Text(
                          'tap to edit profile',
                          style: TextStyle(
                            fontSize: 11,
                            color: Color(0xFF788397),
                          ),
                        ),
                      ],
                    ),
                  ),
                  const Icon(Icons.chevron_right, color: Color(0xFF788397)),
                ],
              ),
            ),
          ),
          Divider(height: 1, color: Theme.of(context).dividerColor),
          Padding(
            padding: const EdgeInsets.fromLTRB(24, 20, 24, 27),
            child: Column(
              children: [
                Row(
                  children: [
                    Container(
                      width: 10,
                      height: 10,
                      decoration: BoxDecoration(
                        color: tracking.isTracking
                            ? fynderGreen
                            : const Color(0xFF98A2B3),
                        shape: BoxShape.circle,
                      ),
                    ),
                    const SizedBox(width: 12),
                    Text(
                      tracking.isTracking ? 'Live' : 'Offline',
                      style: TextStyle(
                        fontSize: 10,
                        color: tracking.isTracking
                            ? fynderGreen
                            : const Color(0xFF98A2B3),
                      ),
                    ),
                    const Spacer(),
                    Text(
                      tracking.isTracking ? 'updated just now' : 'not sharing',
                      style: const TextStyle(
                        fontSize: 10,
                        color: Color(0xFF7A8498),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 30),
                Row(
                  children: [
                    const CircleAvatar(
                      radius: 18,
                      backgroundColor: fynderBlue,
                      child: Icon(
                        Icons.location_on,
                        color: Colors.white,
                        size: 20,
                      ),
                    ),
                    const SizedBox(width: 14),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            coordinate,
                            style: const TextStyle(
                              fontSize: 9,
                              color: Color(0xFF7A8498),
                            ),
                          ),
                          const SizedBox(height: 2),
                          Text(
                            address,
                            style: const TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                          if (tracking.isTracking)
                            const Text(
                              'You’re here right now',
                              style: TextStyle(
                                fontSize: 9,
                                color: fynderBlue,
                                fontWeight: FontWeight.w700,
                              ),
                            ),
                        ],
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _SharingStatus extends StatelessWidget {
  const _SharingStatus({required this.active});
  final bool active;

  @override
  Widget build(BuildContext context) => Container(
    width: double.infinity,
    padding: const EdgeInsets.all(24),
    decoration: BoxDecoration(
      color: Theme.of(context).cardColor,
      borderRadius: BorderRadius.circular(16),
      boxShadow: Theme.of(context).brightness == Brightness.light
          ? const [
              BoxShadow(
                color: Color(0x0D000000),
                blurRadius: 18,
                offset: Offset(0, 8),
              ),
            ]
          : null,
    ),
    child: Row(
      children: [
        Container(
          width: 56,
          height: 56,
          decoration: const BoxDecoration(
            color: Color(0xFFD9FAE8),
            shape: BoxShape.circle,
          ),
          child: Icon(
            active ? Icons.check_circle_outline : Icons.shield_outlined,
            color: fynderGreen,
            size: 28,
          ),
        ),
        const SizedBox(width: 16),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text.rich(
                TextSpan(
                  style: DefaultTextStyle.of(
                    context,
                  ).style.copyWith(fontSize: 12, fontWeight: FontWeight.w700),
                  children: [
                    const TextSpan(text: 'Location sharing is '),
                    TextSpan(
                      text: active ? 'ON' : 'OFF',
                      style: TextStyle(
                        color: active ? fynderGreen : const Color(0xFF98A2B3),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 6),
              Text(
                active
                    ? 'Your location is being shared in real time.'
                    : 'Tap the button above when you’re ready to share.',
                style: const TextStyle(fontSize: 10, color: Color(0xFF7A8498)),
              ),
            ],
          ),
        ),
      ],
    ),
  );
}
