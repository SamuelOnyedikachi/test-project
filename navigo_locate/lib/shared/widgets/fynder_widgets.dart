import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../core/constants/app_assets.dart';
import '../../features/profile/profile_provider.dart';

const fynderBlue = Color(0xFF0759C7);
const fynderGreen = Color(0xFF20C66B);

class FynderHeader extends StatelessWidget {
  const FynderHeader({super.key});

  @override
  Widget build(BuildContext context) {
    final dark = Theme.of(context).brightness == Brightness.dark;
    return Row(
      children: [
        Icon(
          Icons.location_on,
          size: 32,
          color: dark ? Colors.white : Colors.black,
        ),
        const SizedBox(width: 5),
        const Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Fynder',
              style: TextStyle(fontSize: 17, fontWeight: FontWeight.w800),
            ),
            Text(
              'Live Location Sharing',
              style: TextStyle(fontSize: 9, color: Color(0xFF7A8498)),
            ),
          ],
        ),
        const Spacer(),
        const ThemeToggle(),
      ],
    );
  }
}

class ThemeToggle extends StatelessWidget {
  const ThemeToggle({super.key});

  @override
  Widget build(BuildContext context) {
    final profile = context.watch<ProfileProvider>();
    final dark = Theme.of(context).brightness == Brightness.dark;
    return InkWell(
      onTap: profile.toggleTheme,
      borderRadius: BorderRadius.circular(24),
      child: Container(
        width: 56,
        height: 30,
        padding: const EdgeInsets.all(3),
        decoration: BoxDecoration(
          color: dark ? const Color(0xFF071A34) : const Color(0xFF0D1B31),
          borderRadius: BorderRadius.circular(24),
          border: Border.all(
            color: dark ? Colors.transparent : const Color(0xFF0D1B31),
          ),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            _toggleIcon(Icons.light_mode, !dark),
            _toggleIcon(Icons.dark_mode, dark),
          ],
        ),
      ),
    );
  }

  Widget _toggleIcon(IconData icon, bool selected) => Container(
    width: 23,
    height: 23,
    decoration: BoxDecoration(
      color: selected ? Colors.white : Colors.transparent,
      shape: BoxShape.circle,
    ),
    child: Icon(
      icon,
      size: 15,
      color: selected ? const Color(0xFF0D1B31) : Colors.white,
    ),
  );
}

class ProfileAvatar extends StatelessWidget {
  const ProfileAvatar({
    super.key,
    required this.index,
    required this.size,
    this.galleryImage,
  });

  final int index;
  final double size;
  final Uint8List? galleryImage;

  static const _alignments = [
    Alignment(-1, 0),
    Alignment(-0.333, 0),
    Alignment(0.333, 0),
    Alignment(1, 0),
  ];

  @override
  Widget build(BuildContext context) {
    return ClipOval(
      child: SizedBox(
        width: size,
        height: size,
        child: galleryImage != null
            ? Image.memory(galleryImage!, fit: BoxFit.cover)
            : Image.asset(
                AppAssets.avatarSprite,
                fit: BoxFit.cover,
                alignment: _alignments[index.clamp(0, 3)],
              ),
      ),
    );
  }
}

class ControlFooter extends StatelessWidget {
  const ControlFooter({super.key});

  @override
  Widget build(BuildContext context) => const Padding(
    padding: EdgeInsets.symmetric(vertical: 28),
    child: Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Icon(Icons.shield_outlined, size: 17, color: Color(0xFF64789F)),
        SizedBox(width: 8),
        Text(
          "You're in control.",
          style: TextStyle(fontSize: 12, color: Color(0xFF64789F)),
        ),
      ],
    ),
  );
}
