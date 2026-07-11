import 'package:flutter/foundation.dart';
import 'package:uuid/uuid.dart';

import '../../models/contact_permission.dart';
import '../../models/trusted_contact.dart';

class ContactsProvider extends ChangeNotifier {
  final List<TrustedContact> _contacts = [
    const TrustedContact(
      id: 'contact-1',
      name: 'Mother',
      phone: '+234 800 000 0001',
      role: TrustedContactRole.family,
      permissions: ContactPermission.guardian(),
      isVerified: true,
    ),
    const TrustedContact(
      id: 'contact-2',
      name: 'Rescue Desk',
      phone: '+234 800 000 0911',
      role: TrustedContactRole.responder,
      permissions: ContactPermission.responder(),
      isVerified: true,
    ),
  ];

  List<TrustedContact> get contacts => List.unmodifiable(_contacts);

  void addContact({
    required String name,
    required String phone,
    TrustedContactRole role = TrustedContactRole.family,
  }) {
    _contacts.add(
      TrustedContact(
        id: const Uuid().v4(),
        name: name,
        phone: phone,
        role: role,
        permissions: role == TrustedContactRole.responder
            ? const ContactPermission.responder()
            : const ContactPermission.guardian(),
      ),
    );
    notifyListeners();
  }

  void updateContact({
    required String id,
    required String name,
    required String phone,
    required TrustedContactRole role,
  }) {
    final index = _contacts.indexWhere((contact) => contact.id == id);
    if (index == -1) return;

    _contacts[index] = _contacts[index].copyWith(
      name: name,
      phone: phone,
      role: role,
      permissions: role == TrustedContactRole.responder
          ? const ContactPermission.responder()
          : const ContactPermission.guardian(),
    );
    notifyListeners();
  }
}
