import 'dart:typed_data';

import 'package:flutter/material.dart';

import '../auth/auth_service.dart';

class ProfileProvider extends ChangeNotifier {
  ProfileProvider()
    : _name =
          AuthService.currentSession?.user.fullName.trim().isNotEmpty == true
          ? AuthService.currentSession!.user.fullName.trim()
          : (AuthService.currentSession?.user.username ?? 'Gabriel');

  String _name;
  int _avatarIndex = 0;
  Uint8List? _galleryImage;
  ThemeMode _themeMode = ThemeMode.system;

  String get name => _name;
  int get avatarIndex => _avatarIndex;
  Uint8List? get galleryImage => _galleryImage;
  ThemeMode get themeMode => _themeMode;
  bool get isDark => _themeMode == ThemeMode.dark;

  void syncAuthenticatedUser(AuthUser user) {
    final authenticatedName = user.fullName.trim().isNotEmpty
        ? user.fullName.trim()
        : user.username.trim();
    if (authenticatedName.isEmpty || authenticatedName == _name) return;
    _name = authenticatedName;
    notifyListeners();
  }

  void selectAvatar(int index) {
    _avatarIndex = index;
    _galleryImage = null;
    notifyListeners();
  }

  void selectGalleryImage(Uint8List bytes) {
    _galleryImage = bytes;
    notifyListeners();
  }

  void saveName(String value) {
    final nextName = value.trim();
    if (nextName.isEmpty) return;
    _name = nextName;
    notifyListeners();
  }

  void toggleTheme() {
    _themeMode = isDark ? ThemeMode.light : ThemeMode.dark;
    notifyListeners();
  }
}
