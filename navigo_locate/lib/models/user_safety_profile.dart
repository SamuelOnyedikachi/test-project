class UserSafetyProfile {
  const UserSafetyProfile({
    required this.userId,
    required this.fullName,
    required this.phone,
    this.email,
    this.bloodGroup,
    this.allergies = const [],
    this.medicalNotes,
  });

  final String userId;
  final String fullName;
  final String phone;
  final String? email;
  final String? bloodGroup;
  final List<String> allergies;
  final String? medicalNotes;

  Map<String, Object?> toJson() {
    return {
      'userId': userId,
      'fullName': fullName,
      'phone': phone,
      'email': email,
      'bloodGroup': bloodGroup,
      'allergies': allergies,
      'medicalNotes': medicalNotes,
    };
  }
}
