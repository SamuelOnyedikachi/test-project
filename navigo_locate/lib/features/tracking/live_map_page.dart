import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:provider/provider.dart';

import '../../core/constants/app_colors.dart';
import '../../models/destination_route.dart';
import '../../models/location_snapshot.dart';
import '../../models/trusted_contact.dart';
import '../../services/google_maps_loader.dart';
import '../contacts/contacts_provider.dart';
import 'live_tracking_provider.dart';

class LiveMapPage extends StatelessWidget {
  const LiveMapPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer2<LiveTrackingProvider, ContactsProvider>(
      builder: (context, tracking, contacts, _) {
        return Scaffold(
          appBar: AppBar(
            title: const Text('Live Tracking'),
            actions: [
              IconButton(
                tooltip: 'Share live map',
                onPressed: tracking.isTracking
                    ? () => _shareLiveMap(context, tracking, contacts)
                    : null,
                icon: const Icon(Icons.ios_share_outlined),
              ),
              TextButton.icon(
                onPressed: tracking.isTracking
                    ? () async {
                        await tracking.stopTracking();
                        if (context.mounted) {
                          Navigator.pop(context);
                        }
                      }
                    : null,
                icon: const Icon(Icons.stop_circle_outlined),
                label: const Text('Stop'),
              ),
            ],
          ),
          body: Stack(
            children: [
              _MapSurface(tracking: tracking),
              Positioned(
                left: 16,
                right: 16,
                bottom: 16,
                child: _TrackingStatusPanel(
                  tracking: tracking,
                  onShare: tracking.isTracking
                      ? () => _shareLiveMap(context, tracking, contacts)
                      : null,
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
        .toList();
    final agencies = viewers
        .where(
          (contact) =>
              contact.role == TrustedContactRole.responder ||
              contact.role == TrustedContactRole.organization,
        )
        .length;

    final session = tracking.activeSessionId ?? 'current';
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          'Live session $session shared with ${viewers.length} trusted contacts'
          '${agencies > 0 ? ' including $agencies agencies' : ''}.',
        ),
      ),
    );
  }
}

class _MapSurface extends StatefulWidget {
  const _MapSurface({required this.tracking});

  final LiveTrackingProvider tracking;

  @override
  State<_MapSurface> createState() => _MapSurfaceState();
}

class _MapSurfaceState extends State<_MapSurface> {
  GoogleMapController? _controller;
  LatLng? _lastPosition;

  @override
  Widget build(BuildContext context) {
    final location = widget.tracking.latestLocation;
    final route = widget.tracking.destinationRoute;
    final target = location == null
        ? const LatLng(6.5244, 3.3792)
        : LatLng(location.latitude, location.longitude);

    if (!googleMapsReady) {
      return const ColoredBox(
        color: Color(0xFFEFF4FF),
        child: Center(
          child: Padding(
            padding: EdgeInsets.all(24),
            child: Text(
              'Google Maps is not configured for this web build. Add '
              'GOOGLE_MAPS_WEB_API_KEY as a Flutter dart-define.',
              textAlign: TextAlign.center,
            ),
          ),
        ),
      );
    }

    _moveToLatestPosition(target, location != null);

    return GoogleMap(
      initialCameraPosition: CameraPosition(
        target: target,
        zoom: location == null ? 11 : 17,
      ),
      myLocationButtonEnabled: true,
      myLocationEnabled: true,
      mapType: MapType.hybrid,
      onMapCreated: (controller) {
        _controller = controller;
        if (location != null) {
          controller.animateCamera(CameraUpdate.newLatLngZoom(target, 17));
        }
      },
      markers: {
        Marker(
          markerId: const MarkerId('current-location'),
          position: target,
          infoWindow: InfoWindow(
            title: widget.tracking.isEmergency
                ? 'Emergency Location'
                : 'Current Location',
          ),
        ),
        if (route != null)
          Marker(
            markerId: const MarkerId('destination'),
            position: LatLng(route.latitude, route.longitude),
            infoWindow: InfoWindow(title: route.label),
          ),
      },
      polylines: {
        if (route != null && location != null)
          Polyline(
            polylineId: const PolylineId('destination-route'),
            color: AppColors.primary,
            width: 5,
            points: [
              LatLng(location.latitude, location.longitude),
              LatLng(route.latitude, route.longitude),
            ],
          ),
      },
    );
  }

  void _moveToLatestPosition(LatLng target, bool hasLocation) {
    if (!hasLocation || _lastPosition == target) return;
    _lastPosition = target;
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _controller?.animateCamera(CameraUpdate.newLatLng(target));
    });
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }
}

class _TrackingStatusPanel extends StatelessWidget {
  const _TrackingStatusPanel({required this.tracking, required this.onShare});

  final LiveTrackingProvider tracking;
  final VoidCallback? onShare;

  @override
  Widget build(BuildContext context) {
    final location = tracking.latestLocation;
    final route = tracking.destinationRoute;

    return Material(
      elevation: 8,
      borderRadius: BorderRadius.circular(20),
      color: Colors.white,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Icon(
                    tracking.isEmergency
                        ? Icons.sos_rounded
                        : Icons.location_searching_rounded,
                    color: tracking.isEmergency
                        ? AppColors.danger
                        : AppColors.primary,
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Text(
                      tracking.isEmergency
                          ? 'SOS tracking active'
                          : 'Live tracking active',
                      style: const TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                  ),
                  IconButton(
                    tooltip: 'Share live map',
                    onPressed: onShare,
                    icon: const Icon(Icons.ios_share_outlined),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              Text(
                tracking.activeSessionId == null
                    ? 'Session starting...'
                    : 'Session: ${tracking.activeSessionId}',
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(color: AppColors.grey),
              ),
              const SizedBox(height: 10),
              if (location == null)
                const Text('Waiting for first GPS fix...')
              else
                Wrap(
                  spacing: 14,
                  runSpacing: 8,
                  children: [
                    _Metric(
                      label: 'Accuracy',
                      value: '${location.accuracy.toStringAsFixed(0)} m',
                    ),
                    _Metric(
                      label: 'Speed',
                      value: '${location.speed.toStringAsFixed(1)} m/s',
                    ),
                    _Metric(
                      label: 'Heading',
                      value: '${location.heading.toStringAsFixed(0)} deg',
                    ),
                  ],
                ),
              if (route != null) ...[
                const SizedBox(height: 14),
                _RouteSteps(route: route, location: location),
              ],
              if (tracking.errorMessage != null) ...[
                const SizedBox(height: 10),
                Text(
                  tracking.errorMessage!,
                  style: const TextStyle(color: AppColors.danger),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}

class _RouteSteps extends StatelessWidget {
  const _RouteSteps({required this.route, required this.location});

  final DestinationRoute route;
  final LocationSnapshot? location;

  @override
  Widget build(BuildContext context) {
    final currentLocation = location;
    final progress = currentLocation == null
        ? 0.0
        : route.progressFrom(currentLocation);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            const Icon(Icons.flag_outlined, color: AppColors.primary),
            const SizedBox(width: 8),
            Expanded(
              child: Text(
                route.label,
                style: const TextStyle(fontWeight: FontWeight.w800),
              ),
            ),
          ],
        ),
        const SizedBox(height: 8),
        LinearProgressIndicator(value: progress),
        const SizedBox(height: 8),
        for (final step in route.stepsFrom(location))
          Padding(padding: const EdgeInsets.only(bottom: 4), child: Text(step)),
      ],
    );
  }
}

class _Metric extends StatelessWidget {
  const _Metric({required this.label, required this.value});

  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisSize: MainAxisSize.min,
      children: [
        Text(label, style: const TextStyle(color: AppColors.grey)),
        const SizedBox(height: 2),
        Text(value, style: const TextStyle(fontWeight: FontWeight.w700)),
      ],
    );
  }
}
