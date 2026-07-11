enum EmergencyIncidentStatus { active, acknowledged, resolved, falseAlarm }

class EmergencyIncident {
  const EmergencyIncident({
    required this.id,
    required this.userId,
    required this.sessionId,
    required this.status,
    required this.createdAt,
    this.notes,
  });

  final String id;
  final String userId;
  final String sessionId;
  final EmergencyIncidentStatus status;
  final DateTime createdAt;
  final String? notes;

  Map<String, Object?> toJson() {
    return {
      'id': id,
      'userId': userId,
      'sessionId': sessionId,
      'status': status.name,
      'createdAt': createdAt.toUtc().toIso8601String(),
      'notes': notes,
    };
  }
}
