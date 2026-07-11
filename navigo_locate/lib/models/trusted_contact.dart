import 'contact_permission.dart';

enum TrustedContactRole { family, friend, responder, organization }

class TrustedContact {
  const TrustedContact({
    required this.id,
    required this.name,
    required this.phone,
    required this.role,
    required this.permissions,
    this.email,
    this.isVerified = false,
  });

  final String id;
  final String name;
  final String phone;
  final String? email;
  final TrustedContactRole role;
  final ContactPermission permissions;
  final bool isVerified;

  TrustedContact copyWith({
    String? name,
    String? phone,
    String? email,
    TrustedContactRole? role,
    ContactPermission? permissions,
    bool? isVerified,
  }) {
    return TrustedContact(
      id: id,
      name: name ?? this.name,
      phone: phone ?? this.phone,
      email: email ?? this.email,
      role: role ?? this.role,
      permissions: permissions ?? this.permissions,
      isVerified: isVerified ?? this.isVerified,
    );
  }

  Map<String, Object?> toJson() {
    return {
      'id': id,
      'name': name,
      'phone': phone,
      'email': email,
      'role': role.name,
      'permissions': permissions.toJson(),
      'isVerified': isVerified,
    };
  }
}
