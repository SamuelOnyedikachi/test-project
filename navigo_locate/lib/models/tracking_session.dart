import 'location_snapshot.dart';

enum TrackingSessionStatus { active, ended, expired }

class TrackingSession {
  const TrackingSession({
    required this.id,
    required this.userId,
    required this.status,
    required this.startedAt,
    required this.emergency,
    this.endedAt,
    this.latest,
  });

  final String id;
  final String userId;
  final TrackingSessionStatus status;
  final DateTime startedAt;
  final DateTime? endedAt;
  final bool emergency;
  final LocationSnapshot? latest;

  Map<String, Object?> toJson() {
    return {
      'id': id,
      'userId': userId,
      'status': status.name,
      'startedAt': startedAt.toUtc().toIso8601String(),
      'endedAt': endedAt?.toUtc().toIso8601String(),
      'emergency': emergency,
      'latest': latest?.toJson(),
    };
  }
}
