import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/constants/app_colors.dart';
import '../../models/trusted_contact.dart';
import 'contacts_provider.dart';

class ContactsPage extends StatelessWidget {
  const ContactsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<ContactsProvider>(
      builder: (context, provider, _) {
        return Scaffold(
          appBar: AppBar(
            title: const Text('Trusted Contacts'),
            actions: [
              IconButton(
                onPressed: () => _showContactSheet(context),
                icon: const Icon(Icons.person_add_alt_1_outlined),
              ),
            ],
          ),
          body: ListView.separated(
            padding: const EdgeInsets.all(20),
            itemCount: provider.contacts.length,
            separatorBuilder: (_, _) => const SizedBox(height: 12),
            itemBuilder: (context, index) {
              final contact = provider.contacts[index];
              return _ContactTile(
                contact: contact,
                onTap: () => _showContactSheet(context, contact: contact),
              );
            },
          ),
        );
      },
    );
  }

  void _showContactSheet(BuildContext context, {TrustedContact? contact}) {
    final nameController = TextEditingController(text: contact?.name ?? '');
    final phoneController = TextEditingController(text: contact?.phone ?? '');
    var selectedRole = contact?.role ?? TrustedContactRole.family;
    final isEditing = contact != null;

    showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      builder: (sheetContext) {
        return StatefulBuilder(
          builder: (context, setSheetState) {
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
                  Text(
                    isEditing ? 'Edit trusted contact' : 'Add trusted contact',
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    controller: nameController,
                    decoration: const InputDecoration(
                      labelText: 'Name',
                      prefixIcon: Icon(Icons.person_outline),
                    ),
                  ),
                  const SizedBox(height: 12),
                  TextField(
                    controller: phoneController,
                    keyboardType: TextInputType.phone,
                    decoration: const InputDecoration(
                      labelText: 'Phone number',
                      prefixIcon: Icon(Icons.phone_outlined),
                    ),
                  ),
                  const SizedBox(height: 12),
                  DropdownButtonFormField<TrustedContactRole>(
                    initialValue: selectedRole,
                    decoration: const InputDecoration(
                      labelText: 'Role',
                      prefixIcon: Icon(Icons.badge_outlined),
                    ),
                    items: TrustedContactRole.values
                        .map(
                          (role) => DropdownMenuItem(
                            value: role,
                            child: Text(_roleLabel(role)),
                          ),
                        )
                        .toList(),
                    onChanged: (role) {
                      if (role == null) return;
                      setSheetState(() => selectedRole = role);
                    },
                  ),
                  const SizedBox(height: 18),
                  SizedBox(
                    width: double.infinity,
                    height: 52,
                    child: ElevatedButton.icon(
                      onPressed: () {
                        final name = nameController.text.trim();
                        final phone = phoneController.text.trim();
                        if (name.isEmpty || phone.isEmpty) return;

                        final contacts = context.read<ContactsProvider>();
                        if (isEditing) {
                          contacts.updateContact(
                            id: contact.id,
                            name: name,
                            phone: phone,
                            role: selectedRole,
                          );
                        } else {
                          contacts.addContact(
                            name: name,
                            phone: phone,
                            role: selectedRole,
                          );
                        }

                        Navigator.pop(sheetContext);
                      },
                      icon: const Icon(Icons.check_rounded),
                      label: Text(
                        isEditing ? 'Update Contact' : 'Save Contact',
                      ),
                    ),
                  ),
                ],
              ),
            );
          },
        );
      },
    );
  }
}

class _ContactTile extends StatelessWidget {
  const _ContactTile({required this.contact, required this.onTap});

  final TrustedContact contact;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(18),
      child: Ink(
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
              child: Icon(
                contact.role == TrustedContactRole.responder ||
                        contact.role == TrustedContactRole.organization
                    ? Icons.health_and_safety_outlined
                    : Icons.person_outline,
                color: AppColors.primary,
              ),
            ),
            const SizedBox(width: 14),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    contact.name,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    '${_roleLabel(contact.role)} • ${contact.phone}',
                    style: const TextStyle(color: AppColors.grey),
                  ),
                ],
              ),
            ),
            Icon(
              contact.isVerified
                  ? Icons.verified_user_outlined
                  : Icons.hourglass_empty_rounded,
              color: contact.isVerified ? Colors.green : AppColors.grey,
            ),
            const SizedBox(width: 8),
            const Icon(Icons.edit_outlined, color: AppColors.grey),
          ],
        ),
      ),
    );
  }
}

String _roleLabel(TrustedContactRole role) {
  return switch (role) {
    TrustedContactRole.family => 'Family',
    TrustedContactRole.friend => 'Friend',
    TrustedContactRole.responder => 'Responder',
    TrustedContactRole.organization => 'Organization',
  };
}
