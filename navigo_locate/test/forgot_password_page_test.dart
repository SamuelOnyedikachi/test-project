import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:navigo_locate/features/auth/forgot_password_page.dart';

void main() {
  testWidgets('forgot password starts with email request form', (tester) async {
    await tester.pumpWidget(const MaterialApp(home: ForgotPasswordPage()));

    expect(find.text('Forgot your password?'), findsOneWidget);
    expect(find.text('Email address'), findsOneWidget);
    expect(find.text('Send Reset Code'), findsOneWidget);
  });
}
