import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../features/auth/login_page.dart';
import '../features/auth/register_page.dart';
import '../features/contacts/contacts_page.dart';
import '../features/contacts/contacts_provider.dart';
import '../features/history/history_page.dart';
import '../features/home/home_page.dart';
import '../features/notifications/notifications_page.dart';
import '../features/settings/settings_page.dart';
import '../features/splash/splash_page.dart';
import '../features/tracking/live_map_page.dart';
import '../features/tracking/live_tracking_provider.dart';
import 'router.dart';
import 'theme.dart';

class NavigoLocate extends StatelessWidget {
  const NavigoLocate({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => LiveTrackingProvider()),
        ChangeNotifierProvider(create: (_) => ContactsProvider()),
      ],
      child: MaterialApp(
        debugShowCheckedModeBanner: false,
        theme: AppTheme.light,
        initialRoute: Routes.splash,
        routes: {
          Routes.splash: (_) => const SplashPage(),
          Routes.login: (_) => const LoginPage(),
          Routes.register: (_) => const RegisterPage(),
          Routes.home: (_) => const HomePage(),
          Routes.liveMap: (_) => const LiveMapPage(),
          Routes.contacts: (_) => const ContactsPage(),
          Routes.history: (_) => const HistoryPage(),
          Routes.notifications: (_) => const NotificationsPage(),
          Routes.settings: (_) => const SettingsPage(),
        },
      ),
    );
  }
}
