import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:navigo_locate/shared/widgets/info_card.dart';

void main() {
  testWidgets('InfoCard renders title and value', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: InfoCard(
            icon: Icons.gps_fixed,
            title: 'GPS Accuracy',
            value: '12 meters',
            color: Colors.green,
          ),
        ),
      ),
    );

    expect(find.text('GPS Accuracy'), findsOneWidget);
    expect(find.text('12 meters'), findsOneWidget);
  });
}
